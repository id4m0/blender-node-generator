from code_generation import CodeGenerator, CodeGeneratorUtil
import unittest
from unittest import mock
from unittest.mock import patch, mock_open, call


class TestCodeGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_gui = mock.Mock()

    def setUp(self):
        """
        Sets mock gui with default values
        """
        self.mock_gui.get_node_name.return_value = "Node Name"
        self.mock_gui.get_node_type.return_value = "Shader"
        self.mock_gui.get_node_group.return_value = "Shader"
        self.mock_gui.get_source_path.return_value = "C:/some/path"
        self.mock_gui.get_poll.return_value = None
        self.mock_gui.get_node_group_level.return_value = 3
        self.mock_gui.get_node_check_box_count.return_value = 2
        self.mock_gui.get_node_dropdown1_properties.return_value = ["prop1", "prop2"]
        self.mock_gui.get_node_dropdown2_properties.return_value = ["prop2", "prop3"]
        self.mock_gui.get_node_dropdown_property1_name.return_value = "dropdown1"
        self.mock_gui.get_node_dropdown_property2_name.return_value = "dropdown2"
        self.mock_gui.node_has_properties.return_value = True
        self.mock_gui.get_node_check_boxes.return_value = [{"name": "box1", "default": False}, {"name": "box2", "default": True}]
        self.mock_gui.node_has_check_box.return_value = True
        self.mock_gui.get_node_sockets.return_value = [{'type': "Input", 'name': "socket1", 'data_type': "float",
                                                        'min': "-1.0", 'max': "1.0", 'default': "0.0"},
                                                       {'type': "Output", 'name': "socket2", 'data_type': "float",
                                                        'min': "-1.0", 'max': "1.0", 'default': "0.0"}]

    def test_write_osl_file_correct_formatting(self):
        """Test OSL function generation is correct for paramaters"""
        m = mock.MagicMock()
        calls = [call().write('#include "stdosl.h"\n\n'),
                 call().write('shader node_node_name(string dropdown1 = "prop1", '
                                                    'string dropdown2 = "prop2", '
                                                    'int box1 = 0, '
                                                    'int box2 = 1, '
                                                    'float socket1 = 0.0, '
                                                    'output float socket2 = 0.0){}')]

        with patch('builtins.open', mock_open(m)) as mf:
            with patch('code_generation.CodeGeneratorUtil', mock.Mock()):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_osl_shader()
                self.assertTrue(all(c in mf.mock_calls for c in calls))

    def test_write_osl_file_texture_correct_formatting(self):
        """Test OSL function generation is correct for texture node"""
        self.mock_gui.get_node_type.return_value = "Texture"

        m = mock.MagicMock()
        calls = [call().write('#include "stdosl.h"\n\n'),
                 call().write('shader node_node_name_texture(int use_mapping = 0, '
                              'matrix mapping = matrix(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), '
                              'string dropdown1 = "prop1", '
                              'string dropdown2 = "prop2", '
                              'int box1 = 0, '
                              'int box2 = 1, '
                              'float socket1 = 0.0, '
                              'output float socket2 = 0.0){}')]

        with patch('builtins.open', mock_open(m)) as mf:
            with patch('code_generation.CodeGeneratorUtil', mock.Mock()):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_osl_shader()
                self.assertTrue(all(c in mf.mock_calls for c in calls))

    def test_write_to_node_menu_correct_formatting(self):
        with patch('builtins.open', mock_open(read_data=
                        'ShaderNodeCategory("SH_NEW_TEXTURE", "Texture", items=[\n'
                        ']),\n'
                        'ShaderNodeCategory("SH_NEW_SHADER", "Shader", items=[\n'
                        '    NodeItem("ShaderNodeMixShader", poll=eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeAddShader", poll=eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfDiffuse", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfPrincipled", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfGlossy", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfTransparent", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfRefraction", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfGlass", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfTranslucent", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfAnisotropic", poll=object_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfVelvet", poll=object_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfToon", poll=object_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeSubsurfaceScattering", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeEmission", poll=eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfHair", poll=object_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBackground", poll=world_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeHoldout", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeVolumeAbsorption", poll=eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeVolumeScatter", poll=eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeVolumePrincipled"),\n'
                        '    NodeItem("ShaderNodeEeveeSpecular", poll=object_eevee_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfHairPrincipled", poll=object_cycles_shader_nodes_poll)\n'
                        ']),\n'
                        'ShaderNodeCategory("SH_NEW_TEXTURE", "Texture", items=[\n'
                        )) as mf:
            code_gen = CodeGenerator(self.mock_gui)
            code_gen._add_to_node_menu()

            self.assertTrue('        NodeItem("ShaderNodeNodeName")\n' in mf.mock_calls[4][1][0])

    def test_write_to_node_menu_poll_correct_formatting(self):
        self.mock_gui.get_poll.return_value = 'cycles_shader_nodes_poll'
        with patch('builtins.open', mock_open(read_data=
                        'ShaderNodeCategory("SH_NEW_TEXTURE", "Texture", items=[\n'
                        ']),\n'
                        'ShaderNodeCategory("SH_NEW_SHADER", "Shader", items=[\n'
                        '    NodeItem("ShaderNodeMixShader", poll=eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeAddShader", poll=eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfDiffuse", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfPrincipled", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfGlossy", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfTransparent", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfRefraction", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfGlass", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfTranslucent", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfAnisotropic", poll=object_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfVelvet", poll=object_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfToon", poll=object_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeSubsurfaceScattering", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeEmission", poll=eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfHair", poll=object_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBackground", poll=world_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeHoldout", poll=object_eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeVolumeAbsorption", poll=eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeVolumeScatter", poll=eevee_cycles_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeVolumePrincipled"),\n'
                        '    NodeItem("ShaderNodeEeveeSpecular", poll=object_eevee_shader_nodes_poll),\n'
                        '    NodeItem("ShaderNodeBsdfHairPrincipled", poll=object_cycles_shader_nodes_poll)\n'
                        ']),\n'
                        'ShaderNodeCategory("SH_NEW_TEXTURE", "Texture", items=[\n'
                        )) as mf:
            code_gen = CodeGenerator(self.mock_gui)
            code_gen._add_to_node_menu()

            self.assertTrue('        NodeItem("ShaderNodeNodeName", poll=cycles_shader_nodes_poll)\n' in mf.mock_calls[4][1][0])

    def test_write_node_id_correct_formatting(self):
        with patch('builtins.open', mock_open(read_data=    '#define SH_NODE_TEX_WHITE_NOISE 704\n'
                                                            '#define SH_NODE_VOLUME_INFO 705\n'
                                                            '#define SH_NODE_VERTEX_COLOR 706\n'
                                                            '\n'
                                                            '/* custom defines options for Material node */\n'
                                                            '#define SH_NODE_MAT_DIFF 1\n'
                                                            '#define SH_NODE_MAT_SPEC 2\n'
                                                            '#define SH_NODE_MAT_NEG 4\n'
                                                            )) as mf:
            code_gen = CodeGenerator(self.mock_gui)
            code_gen._add_node_type_id()
            self.assertTrue(mf.mock_calls[-3][1][0] ==      '#define SH_NODE_TEX_WHITE_NOISE 704\n'
                                                            '#define SH_NODE_VOLUME_INFO 705\n'
                                                            '#define SH_NODE_VERTEX_COLOR 706\n'
                                                            '#define SH_NODE_NODE_NAME 707\n'
                                                            '\n'
                                                            '/* custom defines options for Material node */\n'
                                                            '#define SH_NODE_MAT_DIFF 1\n'
                                                            '#define SH_NODE_MAT_SPEC 2\n'
                                                            '#define SH_NODE_MAT_NEG 4\n')

    def test_write_dna_struct_correct_formatting(self):
        self.mock_gui.get_node_type.return_value = "Texture"
        with patch('builtins.open', mock_open(read_data='typedef struct NodeTexWave {\n'
                                                        '  NodeTexBase base;\n'
                                                        '  int wave_type;\n'
                                                        '  int wave_profile;\n'
                                                        '} NodeTexWave;\n'
                                                        '\n'
                                                        'typedef struct NodeTexMagic {\n'
                                                        '  NodeTexBase base;\n'
                                                        '  int depth;\n'
                                                        '  char _pad[4];\n'
                                                        '} NodeTexMagic;\n'
                                                        '\n'
                                                        'typedef struct NodeShaderAttribute {\n'
                                                        '  char name[64];\n'
                                                        '} NodeShaderAttribute;\n')) as mf:
            with patch('code_generation.CodeGeneratorUtil', mock.Mock()):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_dna_node_type()

                self.assertTrue(mf.mock_calls[-3][1][0] == 'typedef struct NodeTexWave {\n'
                                                            '  NodeTexBase base;\n'
                                                            '  int wave_type;\n'
                                                            '  int wave_profile;\n'
                                                            '} NodeTexWave;\n'
                                                            '\n'
                                                            'typedef struct NodeTexMagic {\n'
                                                            '  NodeTexBase base;\n'
                                                            '  int depth;\n'
                                                            '  char _pad[4];\n'
                                                            '} NodeTexMagic;\n'
                                                            '\n'
                                                            'typedef struct NodeTexNodeName {NodeTexBase base; int dropdown1; int dropdown2; int box1; int box2;} NodeTexNodeName;\n'
                                                            '\n'
                                                            'typedef struct NodeShaderAttribute {\n'
                                                            '  char name[64];\n'
                                                            '} NodeShaderAttribute;\n')

    def test_write_dna_struct_requires_padding_correct_formatting(self):
        self.mock_gui.get_node_type.return_value = "Texture"
        self.mock_gui.get_node_check_boxes.return_value = [{"name": "box1", "default": False}]
        self.mock_gui.get_node_check_box_count.return_value = 1
        with patch('builtins.open', mock_open(read_data='typedef struct NodeTexWave {\n'
                                                        '  NodeTexBase base;\n'
                                                        '  int wave_type;\n'
                                                        '  int wave_profile;\n'
                                                        '} NodeTexWave;\n'
                                                        '\n'
                                                        'typedef struct NodeTexMagic {\n'
                                                        '  NodeTexBase base;\n'
                                                        '  int depth;\n'
                                                        '  char _pad[4];\n'
                                                        '} NodeTexMagic;\n'
                                                        '\n'
                                                        'typedef struct NodeShaderAttribute {\n'
                                                        '  char name[64];\n'
                                                        '} NodeShaderAttribute;\n')) as mf:
            with patch('code_generation.CodeGeneratorUtil', mock.Mock()):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_dna_node_type()

                self.assertTrue(mf.mock_calls[-3][1][0] == 'typedef struct NodeTexWave {\n'
                                                            '  NodeTexBase base;\n'
                                                            '  int wave_type;\n'
                                                            '  int wave_profile;\n'
                                                            '} NodeTexWave;\n'
                                                            '\n'
                                                            'typedef struct NodeTexMagic {\n'
                                                            '  NodeTexBase base;\n'
                                                            '  int depth;\n'
                                                            '  char _pad[4];\n'
                                                            '} NodeTexMagic;\n'
                                                            '\n'
                                                            'typedef struct NodeTexNodeName {NodeTexBase base; int dropdown1; int dropdown2; int box1; char _pad[4];} NodeTexNodeName;\n'
                                                            '\n'
                                                            'typedef struct NodeShaderAttribute {\n'
                                                            '  char name[64];\n'
                                                            '} NodeShaderAttribute;\n')

    def test_write_dna_struct_not_texture_no_call(self):
        with patch('builtins.open', mock_open()) as mf:
            code_gen = CodeGenerator(self.mock_gui)
            code_gen._add_dna_node_type()

            self.assertTrue(len(mf.mock_calls) == 0)

    def test_write_drawnode_correct_formatting(self):
        with patch('builtins.open', mock_open(read_data=
                 'static void node_shader_buts_white_noise(uiLayout *layout, bContext *UNUSED(C), PointerRNA *ptr)\n'
                 '{\n'
                 '  uiItemR(layout, ptr, "noise_dimensions", 0, "", ICON_NONE);\n'
                 '}\n'
                 '\n'
                 '/ * only once called * /\n'
                 'static void node_shader_set_butfunc(bNodeType *ntype)\n'
                 '{\n'
                 '   switch (ntype->type) {\n'
                 '       case SH_NODE_TEX_WHITE_NOISE:\n'
                 '           ntype->draw_buttons = node_shader_buts_white_noise;\n'
                 '           break;\n'
                 '       case SH_NODE_TEX_TRUCHET:\n'
                 '           ntype->draw_buttons = node_shader_buts_truchet;\n'
                 '           break;\n'
                 '   }\n'
                 '}\n')) as mf:
            with patch('code_generation.CodeGeneratorUtil', mock.Mock()):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_node_drawing()

            self.assertTrue('static void node_shader_buts_node_name(uiLayout *layout, bContext *UNUSED(C), PointerRNA *ptr)'
                            '{uiItemR(layout, ptr, "dropdown1", 0, "", ICON_NONE);'
                            'uiItemR(layout, ptr, "dropdown2", 0, "", ICON_NONE);'
                            'uiItemR(layout, ptr, "box1", 0, NULL, ICON_NONE);'
                            'uiItemR(layout, ptr, "box2", 0, NULL, ICON_NONE);}\n\n' in mf.mock_calls[-3][1][0]
                            and 'case SH_NODE_NODE_NAME:\n' in mf.mock_calls[-3][1][0]
                            and 'ntype->draw_buttons = node_shader_buts_node_name;\n' in mf.mock_calls[-3][1][0])

    def test_write_drawnode_texture_correct_formatting(self):
        self.mock_gui.get_node_type.return_value = "Texture"
        with patch('builtins.open', mock_open(read_data=
                 'static void node_shader_buts_white_noise(uiLayout *layout, bContext *UNUSED(C), PointerRNA *ptr)\n'
                 '{\n'
                 '  uiItemR(layout, ptr, "noise_dimensions", 0, "", ICON_NONE);\n'
                 '}\n'
                 '\n'
                 '/ * only once called * /\n'
                 'static void node_shader_set_butfunc(bNodeType *ntype)\n'
                 '{\n'
                 '   switch (ntype->type) {\n'
                 '       case SH_NODE_TEX_WHITE_NOISE:\n'
                 '           ntype->draw_buttons = node_shader_buts_white_noise;\n'
                 '           break;\n'
                 '       case SH_NODE_TEX_TRUCHET:\n'
                 '           ntype->draw_buttons = node_shader_buts_truchet;\n'
                 '           break;\n'
                 '   }\n'
                 '}\n')) as mf:
            with patch('code_generation.CodeGeneratorUtil', mock.Mock()):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_node_drawing()

            self.assertTrue('static void node_shader_buts_node_name(uiLayout *layout, bContext *UNUSED(C), PointerRNA *ptr)'
                            '{uiItemR(layout, ptr, "dropdown1", 0, "", ICON_NONE);'
                            'uiItemR(layout, ptr, "dropdown2", 0, "", ICON_NONE);'
                            'uiItemR(layout, ptr, "box1", 0, NULL, ICON_NONE);'
                            'uiItemR(layout, ptr, "box2", 0, NULL, ICON_NONE);}\n\n' in mf.mock_calls[-3][1][0]
                            and 'case SH_NODE_TEX_NODE_NAME:\n' in mf.mock_calls[-3][1][0]
                            and 'ntype->draw_buttons = node_shader_buts_tex_node_name;\n' in mf.mock_calls[-3][1][0])

    def test_write_node_class_correct_formatting(self):
        with patch('builtins.open', mock_open()) as mf:
            with patch('code_generation.CodeGeneratorUtil.apply_clang_formatting'):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_cycles_class()

                self.assertTrue(mf.mock_calls[-2][1][0] == 'class NodeNameNode : public ShaderNode {'
                                                           'public:SHADER_NODE_CLASS(NodeNameNode)'
                                                           'virtual int get_group(){return NODE_GROUP_LEVEL_3;}'
                                                           'float socket1;'
                                                           'bool box1, box2;'
                                                           'int dropdown1, dropdown2;};')

    def test_write_node_class_level_0_correct_formatting(self):
        self.mock_gui.get_node_group_level.return_value = 0
        with patch('builtins.open', mock_open()) as mf:
            with patch('code_generation.CodeGeneratorUtil.apply_clang_formatting'):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_cycles_class()

                self.assertTrue(mf.mock_calls[-2][1][0] == 'class NodeNameNode : public ShaderNode {'
                                                           'public:SHADER_NODE_CLASS(NodeNameNode)'
                                                           'float socket1;'
                                                           'bool box1, box2;'
                                                           'int dropdown1, dropdown2;};')

    def test_write_node_class_no_check_boxes_correct_formatting(self):
        self.mock_gui.get_node_check_boxes.return_value = []
        self.mock_gui.node_has_check_box.return_value = False
        with patch('builtins.open', mock_open()) as mf:
            with patch('code_generation.CodeGeneratorUtil.apply_clang_formatting'):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_cycles_class()

                self.assertTrue(mf.mock_calls[-2][1][0] == 'class NodeNameNode : public ShaderNode {'
                                                           'public:SHADER_NODE_CLASS(NodeNameNode)'
                                                           'virtual int get_group(){return NODE_GROUP_LEVEL_3;}'
                                                           'float socket1;'
                                                           'int dropdown1, dropdown2;};')

    def test_write_node_class_no_dropdowns_correct_formatting(self):
        self.mock_gui.get_node_dropdown_property1_name.return_value = None
        self.mock_gui.get_node_dropdown_property2_name.return_value = None
        with patch('builtins.open', mock_open()) as mf:
            with patch('code_generation.CodeGeneratorUtil.apply_clang_formatting'):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_cycles_class()

                self.assertTrue(mf.mock_calls[-2][1][0] == 'class NodeNameNode : public ShaderNode {'
                                                           'public:SHADER_NODE_CLASS(NodeNameNode)'
                                                           'virtual int get_group(){return NODE_GROUP_LEVEL_3;}'
                                                           'float socket1;'
                                                           'bool box1, box2;};')

    def test_write_node_class_no_sockets_correct_formatting(self):
        self.mock_gui.get_node_sockets.return_value = []
        with patch('builtins.open', mock_open()) as mf:
            with patch('code_generation.CodeGeneratorUtil.apply_clang_formatting'):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_cycles_class()

                self.assertTrue(mf.mock_calls[-2][1][0] == 'class NodeNameNode : public ShaderNode {'
                                                           'public:SHADER_NODE_CLASS(NodeNameNode)'
                                                           'virtual int get_group(){return NODE_GROUP_LEVEL_3;}'
                                                           'bool box1, box2;'
                                                           'int dropdown1, dropdown2;};')

    def test_write_node_class_no_props_correct_formatting(self):
        self.mock_gui.get_node_sockets.return_value = []
        self.mock_gui.get_node_dropdown_property1_name.return_value = None
        self.mock_gui.get_node_dropdown_property2_name.return_value = None
        self.mock_gui.get_node_check_boxes.return_value = []
        self.mock_gui.node_has_check_box.return_value = False
        with patch('builtins.open', mock_open()) as mf:
            with patch('code_generation.CodeGeneratorUtil.apply_clang_formatting'):
                code_gen = CodeGenerator(self.mock_gui)
                code_gen._add_cycles_class()

                self.assertTrue(mf.mock_calls[-2][1][0] == 'class NodeNameNode : public ShaderNode {'
                                                           'public:SHADER_NODE_CLASS(NodeNameNode)'
                                                           'virtual int get_group(){return NODE_GROUP_LEVEL_3;}};')


if __name__ == "__main__":
    unittest.main()
