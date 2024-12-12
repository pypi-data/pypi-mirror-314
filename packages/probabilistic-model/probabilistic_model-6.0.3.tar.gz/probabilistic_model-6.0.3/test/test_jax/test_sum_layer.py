import unittest

import numpy as np
from jax.experimental.sparse import BCOO, BCSR
from random_events.interval import closed
from random_events.product_algebra import SimpleEvent
from random_events.variable import Continuous
import jax.numpy as jnp
from sortedcontainers import SortedSet

from probabilistic_model.learning.nyga_distribution import NygaDistribution
from probabilistic_model.probabilistic_circuit.jax.input_layer import DiracDeltaLayer
from probabilistic_model.probabilistic_circuit.jax.inner_layer import SumLayer
import jax

from probabilistic_model.probabilistic_circuit.jax.probabilistic_circuit import ProbabilisticCircuit
from probabilistic_model.probabilistic_circuit.nx.probabilistic_circuit import ProbabilisticCircuit as NXProbabilisticCircuit


class DiracSumUnitTestCase(unittest.TestCase):
    x: Continuous = Continuous("x")

    p1_x = DiracDeltaLayer(0, jnp.array([0., 1.]), jnp.array([1, 2]))
    p2_x = DiracDeltaLayer(0,jnp.array([2.]), jnp.array([3]))
    p3_x = DiracDeltaLayer(0, jnp.array([3., 4., 5.]), jnp.array([4, 5, 6]))
    p4_x = DiracDeltaLayer(0, jnp.array([6.]), jnp.array([1]))
    sum_layer: SumLayer

    @classmethod
    def setUpClass(cls):
        weights_p1 = BCOO.fromdense(jnp.array([[0, 0.1], [0.4, 0]])) * 2
        weights_p1.data = jnp.log(weights_p1.data)

        weights_p2 = BCOO.fromdense(jnp.array([[0.2], [0.3]])) * 2
        weights_p2.data = jnp.log(weights_p2.data)

        weights_p3 = BCOO.fromdense(jnp.array([[0.3, 0, 0.4], [0., 0.1, 0.2]])) * 2
        weights_p3.data = jnp.log(weights_p3.data)

        weights_p4 = BCOO.fromdense(jnp.array([[0], [0]])) * 2
        weights_p4.data = jnp.log(weights_p4.data)

        cls.sum_layer = SumLayer([cls.p1_x, cls.p2_x, cls.p3_x, cls.p4_x],
                                 log_weights=[weights_p1, weights_p2, weights_p3, weights_p4])
        cls.sum_layer.validate()

    def test_normalization_constants(self):
        log_normalization_constants = self.sum_layer.log_normalization_constants
        result = jnp.log(jnp.array([2, 2]))
        self.assertTrue(jnp.allclose(log_normalization_constants, result))

    def test_normalized_weights(self):
        normalized_weights = self.sum_layer.normalized_weights.todense()
        result = jnp.array([[0, 0.1, 0.2, 0.3, 0, 0.4, 0],
                            [0.4, 0, 0.3, 0., 0.1, 0.2, 0]])
        self.assertTrue(jnp.allclose(normalized_weights, result))

    def test_ll(self):
        data = jnp.array([0., 1., 2., 3., 4., 5., 6.]).reshape(-1, 1)
        # l = self.sum_layer.log_likelihood_of_nodes_single(data[0])

        ll = self.sum_layer.log_likelihood_of_nodes(data)
        result = jnp.log(jnp.array([[0., 0.4,],
                               [0.1 * 2, 0.,],
                               [0.2 * 3, 0.3 * 3,],
                               [0.3 * 4, 0.,],
                               [0., 0.1 * 5,],
                               [0.4 * 6, 0.2 * 6,],
                               [0., 0.,]]))
        assert jnp.allclose(ll, result)

    def test_cdf(self):
        data = jnp.arange(7, dtype=jnp.float32).reshape(-1, 1) - 0.5
        cdf = self.sum_layer.cdf_of_nodes(data)
        self.assertEqual(cdf.shape, (7, 2))
        result = jnp.array([[0, 0], # -0.5
                               [0, 0.4], # 0.5
                               [0.1, 0.4], # 1.5
                               [0.3, 0.7], # 2.5
                               [0.6, 0.7], # 3.5
                               [0.6, 0.8], # 4.5
                               [1, 1], # 5.5
                               ], dtype=jnp.float32)
        self.assertTrue(jnp.allclose(cdf, result))

    def test_moment(self):
        order = jnp.array([1], dtype=jnp.int32)
        center = jnp.array([2.5], dtype=jnp.float32)
        moment = self.sum_layer.moment_of_nodes(order, center)
        result = jnp.array([0.9, -0.5], dtype=jnp.float32).reshape(-1, 1)
        self.assertTrue(jnp.allclose(moment, result))

    def test_probability(self):
        event = SimpleEvent({self.x: closed(0.5, 2.5) | closed(4.5, 10)})
        prob = self.sum_layer.probability_of_simple_event(event)
        result = jnp.array([0.7, 0.5], dtype=jnp.float32)
        self.assertTrue(jnp.allclose(result, prob))

    def test_conditional(self):
        event = SimpleEvent({self.x: closed(0.5, 1.5)})
        c, lp = self.sum_layer.log_conditional_of_simple_event(event)
        c.validate()
        self.assertEqual(c.number_of_nodes, 1)
        self.assertEqual(len(c.child_layers), 1)
        self.assertEqual(c.child_layers[0].number_of_nodes, 1)
        self.assertTrue(jnp.allclose(c.log_weights[0].todense(), jnp.array([[0.]])))
        self.assertTrue(jnp.allclose(lp, jnp.log(jnp.array([0.1, 0.]))))

    def test_conditional_2(self):
        event = SimpleEvent({self.x: closed(1.5, 4.5)})
        c, lp = self.sum_layer.log_conditional_of_simple_event(event)
        c.validate()
        self.assertEqual(c.number_of_nodes, 2)
        self.assertEqual(len(c.child_layers), 2)
        self.assertEqual(c.child_layers[0].number_of_nodes, 1)
        self.assertEqual(c.child_layers[1].number_of_nodes, 2)

    def test_remove(self):
        result = self.sum_layer.remove_nodes(jnp.array([True, False]))
        result.validate()
        self.assertEqual(result.number_of_nodes, 1)


class PCSumUnitTestCase(unittest.TestCase):
    x: Continuous = Continuous("x")

    p1_x = DiracDeltaLayer(0, jnp.array([0., 1.]), jnp.array([1, 2]))
    p2_x = DiracDeltaLayer(0,jnp.array([2.]), jnp.array([3]))
    p3_x = DiracDeltaLayer(0, jnp.array([3., 4., 5.]), jnp.array([4, 5, 6]))
    p4_x = DiracDeltaLayer(0, jnp.array([6.]), jnp.array([1]))
    model: ProbabilisticCircuit

    @classmethod
    def setUpClass(cls):
        weights_p1 = BCOO.fromdense(jnp.array([[0, 0.1]])) * 2
        weights_p1.data = jnp.log(weights_p1.data)

        weights_p2 = BCOO.fromdense(jnp.array([[0.2]])) * 2
        weights_p2.data = jnp.log(weights_p2.data)

        weights_p3 = BCOO.fromdense(jnp.array([[0.3, 0, 0.4]])) * 2
        weights_p3.data = jnp.log(weights_p3.data)

        weights_p4 = BCOO.fromdense(jnp.array([[0]])) * 2
        weights_p4.data = jnp.log(weights_p4.data)

        sum_layer = SumLayer([cls.p1_x, cls.p2_x, cls.p3_x, cls.p4_x],
                                 log_weights=[weights_p1, weights_p2, weights_p3, weights_p4])
        sum_layer.validate()
        cls.model = ProbabilisticCircuit(SortedSet([cls.x]), sum_layer)

    def test_sampling(self):
        np.random.seed(69)
        samples = self.model.sample(10)
        self.assertEqual(samples.shape, (10, 1))
        result = np.array([2, 2, 2, 3, 3, 5, 5, 5, 5, 5]).reshape(-1, 1)
        self.assertTrue(np.allclose(samples, result))

    def test_conditioning(self):
        event = SimpleEvent({self.x: closed(1.5, 4.5)})
        conditional, log_prob = self.model.root.log_conditional_of_simple_event(event)
        # conditional.validate()


class NygaDistributionTestCase(unittest.TestCase):

    nx_model: NXProbabilisticCircuit
    jax_model: ProbabilisticCircuit
    data: jax.Array

    @classmethod
    def setUpClass(cls):
        cls.data = jax.random.normal(jax.random.PRNGKey(69), (1000, 1))
        model = NygaDistribution(Continuous("x"), min_samples_per_quantile=10)
        model.fit(cls.data)
        cls.nx_model = model
        cls.jax_model = ProbabilisticCircuit.from_nx(cls.nx_model)
        cls.jax_model.root.validate()

    def test_log_likelihood(self):
        ll = self.jax_model.log_likelihood(self.data)
        self.assertTrue(jnp.all(ll > -jnp.inf))

    def test_sampling(self):
        data = self.jax_model.sample(1000)
        self.assertEqual(data.shape, (1000, 1))