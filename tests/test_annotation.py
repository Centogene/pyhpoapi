import os
import unittest
from unittest.mock import patch, MagicMock

from pyhpo.ontology import Ontology

from fastapi.testclient import TestClient
from pyhpoapi.server import main

client = TestClient(main())


class OmimTests(unittest.TestCase):
    def setUp(self):
        folder = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            'data'
        )
        _ = Ontology(data_folder=folder)

    def test_single_omim(self):
        response = client.get('/omim/600001')
        self.assertEqual(
            response.json(),
            {'id': 600001, 'name': 'Disease 1', 'hpo': None}
        )

        response = client.get('/omim/600001?verbose=True')
        self.assertIsNot(
            response.json()['hpo'],
            None
        )

    def test_missing_omim(self):
        response = client.get('/omim/600011')
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            response.json(),
            {'detail': 'OMIM disease does not exist'}
        )

    def test_omim_similarity(self):
        response = client.get(
            '/similarity/omim?set1=HP:0021,HP:0013,HP:0031&omim=600001'
        )
        res = response.json()
        self.assertIn('set1', res)
        self.assertIn('set2', res)
        self.assertIn('omim', res)
        self.assertIn('similarity', res)
        self.assertEqual(len(res['set1']), 3)
        self.assertEqual(len(res['set2']), 2)

        response = client.get(
            '/similarity/omim?set1=HP:0021,HP:0013,HP:0031&omim=6666'
        )
        res = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            res,
            {'detail': 'OMIM disease does not exist'}
        )


class GeneTests(unittest.TestCase):
    def setUp(self):
        folder = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            'data'
        )
        _ = Ontology(data_folder=folder)

    def test_single_gene(self):
        response = client.get('/gene/Gene1')
        self.assertEqual(
            response.json(),
            {'id': 1, 'name': 'Gene1', 'symbol': 'Gene1', 'hpo': None}
        )

        response = client.get('/gene/Gene1?verbose=True')
        self.assertIsNot(
            response.json()['hpo'],
            None
        )

    def test_missing_gene(self):
        response = client.get('/gene/27')
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            response.json(),
            {'detail': 'Gene does not exist'}
        )

    def test_gene_similarity(self):
        response = client.get(
            '/similarity/gene?set1=HP:0021,HP:0013,HP:0031&gene=Gene1'
        )
        res = response.json()
        self.assertIn('set1', res)
        self.assertIn('set2', res)
        self.assertIn('gene', res)
        self.assertIn('similarity', res)
        self.assertEqual(len(res['set1']), 3)
        self.assertEqual(len(res['set2']), 2)

        response = client.get(
            '/similarity/gene?set1=HP:0021,HP:0013,HP:0031&gene=FooBar'
        )
        res = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            res,
            {'detail': 'Gene does not exist'}
        )