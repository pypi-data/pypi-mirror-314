import json
import tempfile
import unittest
import builtins
import aidge_core
from pathlib import Path
from aidge_core.show_graphview import gview_to_json

def create_gview():
    # Create a LeNet-like model
    gview = aidge_core.sequential([aidge_core.PaddedConv2D(in_channels=1, out_channels=6, kernel_dims=[5,5], name='feature_feature_0_Conv', stride_dims=[1,1], padding_dims = [2,2,2,2]),
                               aidge_core.ReLU(name='feature_feature_1_Relu'),
                               aidge_core.MaxPooling2D(kernel_dims=[2,2], stride_dims=[2,2], ceil_mode=0, name='feature_feature_2_MaxPool'),
                               aidge_core.Conv2D(in_channels=6, out_channels=16, kernel_dims=[5,5], name='feature_feature_3_Conv', stride_dims=[1,1], dilation_dims = [1,1]),
                               aidge_core.ReLU(name='feature_feature_4_Relu'),
                               aidge_core.MaxPooling2D(kernel_dims=[2,2], stride_dims=[2,2], ceil_mode=0, name='feature_feature_5_MaxPool'),
                               aidge_core.FC(in_channels=400, out_channels=120, name='classifier_classifier_1_Gemm'),
                               aidge_core.ReLU(name='classifier_classifier_2_Relu'),
                               aidge_core.FC(in_channels=120, out_channels=84, name='classifier_classifier_3_Gemm'),
                               aidge_core.ReLU(name='classifier_classifier_4_Relu'),
                               aidge_core.FC(in_channels=84, out_channels=10, name='classifier_classifier_5_Gemm'),
                            ])

    # Fill Producers
    for node in gview.get_nodes():
        if node.type() == "Producer":
            prod_op = node.get_operator()
            value = prod_op.get_output(0)
            value.set_backend("cpu")
            tuple_out = node.output(0)[0]
            
            if (tuple_out[0].type() == "Conv" or tuple_out[0].type() == "PaddedConv") and tuple_out[1]==1:
                # Conv weight
                aidge_core.xavier_uniform_filler(value)
            elif tuple_out[0].type() == "Conv" and tuple_out[1]==2:
                # Conv bias
                aidge_core.constant_filler(value, 0.01)
            elif tuple_out[0].type() == "FC" and tuple_out[1]==1:
                # FC weight
                aidge_core.normal_filler(value)
            elif tuple_out[0].type() == "FC" and tuple_out[1]==2:
                # FC bias
                aidge_core.constant_filler(value, 0.01)
            else:
                pass

    # Compile model
    gview.forward_dims([[1, 1, 28, 28]]) 
    gview.set_datatype(aidge_core.dtype.float32)

    return gview

class test_show_gview(unittest.TestCase):
    """Test aidge functionality to show GraphView.    
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gview_to_json(self):
        
        gview = create_gview()

        # Create temporary file to store JSON model description             
        model_description_file = tempfile.NamedTemporaryFile(mode="w+", suffix='.json')

        gview_to_json(gview, Path(model_description_file.name))

        # Load JSON
        with open(model_description_file.name, 'r') as fp:
                model_json = json.load(fp)

        # Get list of nodes of Aidge graphview
        gview_ordered_nodes = gview.get_ordered_nodes()

        # Iterate over the list of ordered nodes and the corresponding JSON 
        self.assertEqual(len(gview_ordered_nodes), len(model_json['graph']))

        for node_gview, node_json in zip(gview_ordered_nodes, model_json['graph']):   
                    
            self.assertEqual(node_gview.get_operator().type(), node_json['optype'])
            self.assertEqual(node_gview.get_operator().nb_inputs(), node_json['nb_inputs'])
            self.assertEqual(node_gview.get_operator().nb_outputs(), node_json['nb_outputs'])
            
            self.assertEqual(node_gview.get_operator().nb_inputs(), len(node_json['inputs']))
            for input_idx in range(node_gview.get_operator().nb_inputs()):
                self.assertEqual(node_gview.get_operator().get_input(input_idx).dims(), node_json['inputs'][input_idx]['dims'])
                self.assertEqual(str(node_gview.get_operator().get_input(input_idx).dtype()), node_json['inputs'][input_idx]['data_type'])
                self.assertEqual(str(node_gview.get_operator().get_input(input_idx).dformat()), node_json['inputs'][input_idx]['data_format'])

            self.assertEqual(node_gview.get_operator().nb_outputs(), len(node_json['outputs']))
            for output_idx in range(node_gview.get_operator().nb_outputs()):
                self.assertEqual(node_gview.get_operator().get_output(output_idx).dims(), node_json['outputs'][output_idx]['dims'])
                self.assertEqual(str(node_gview.get_operator().get_output(output_idx).dtype()), node_json['outputs'][output_idx]['data_type'])
                self.assertEqual(str(node_gview.get_operator().get_output(output_idx).dformat()), node_json['outputs'][output_idx]['data_format'])

            self.assertEqual(len(node_gview.get_parents()), len(node_json['parents']))                  
            self.assertEqual(len(node_gview.get_children()), len(node_json['children']))

            if not hasattr(node_gview.get_operator(), 'get_micro_graph'):
                try:
                    self.assertEqual(len(node_gview.get_operator().attr.dict()), len(node_json['attributes']))
                    self.assertDictEqual(node_gview.get_operator().attr.dict(), node_json['attributes'])

                except AttributeError:
                    self.assertIsNone(node_gview.get_operator().attr) and self.assertFalse(node_json['attributes'])

            elif hasattr(node_gview.get_operator(), 'get_micro_graph'):
                
                self.assertEqual(len(node_gview.get_operator().get_micro_graph().get_nodes()), len(node_json['attributes']['micro_graph']))
                
                for micro_node_gview in node_gview.get_operator().get_micro_graph().get_nodes():
                    for micro_node_json in node_json['attributes']['micro_graph']:
                        if micro_node_gview.get_operator().type() == micro_node_json['optype']:
                            
                            for key, value in micro_node_gview.get_operator().attr.dict().items():
                                if not type(value).__name__ in dir(builtins):
                                    # Replace original value by its name (str) because value is of a type that could not be written to the JSON
                                    # Cannot update this dict inplace : micro_node_gview.get_operator().attr.dict().update({key : value.name}) 
                                    temp_mnode_dict = micro_node_gview.get_operator().attr.dict()
                                    temp_mnode_dict.update({key : value.name})
                                    self.assertDictEqual(temp_mnode_dict, micro_node_json['attributes'])                
                    
if __name__ == '__main__':
    unittest.main()

