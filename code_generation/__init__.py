class CodeGenerator:
    """Generates code required for a new node"""
    def __init__(self, gui):
        self._gui = gui

    def _add_node_type_ID(self):
        """BKE_node.h"""
        with open("/".join((self._gui.get_source_path(), "source", "blender", "blenderkernel", "BKE_node.h")), "r") as f:
            last = 707
            name_underscored = "_".join(self._gui.get_node_name().split(" "))
            line = "#define SH_NODE_" + ("TEX_" if self._gui.get_node_type() == "Texture" else "") + name_underscored.upper() + " " + str(last+1)
            print(line)

    def _add_DNA_node_type(self):
        """
        DNA_node_types.h
        For texture nodes
        """
        pass

    def _add_rna_properties(self):
        """rna_nodetree.c"""
        pass

    def _add_node_definition(self):
        """NOD_static_types.h"""
        with open("/".join((self._gui.get_source_path(), "source", "blender", "nodes", "NOD_static_types.h")), "r") as f:
            lines = f.readlines()

            node_name_underscored = self._gui.get_node_name().replace(" ", "_")

            node_definition = 'DefNode(ShaderNode,     ' + \
                              'SH_NODE_' + "_".join(("TEX" if self._gui.get_node_type() == "Texture" else "", node_name_underscored.upper())) + \
                              ',' + ('def_sh_' + node_name_underscored.lower() if self._gui.node_has_properties() else '0') + \
                              ', ' + ('Tex' if self._gui.get_node_type() == "Texture" else '') + self._gui.get_node_name().replace(" ", "") + \
                              ', ' + " ".join(map(lambda word: word.capitalize(), self._gui.get_node_name().split(" "))) + ',  ""   ' + ")"
            print(node_definition)

    def _add_node_drawing(self):
        """drawnode.c"""
        if self._gui.node_has_properties() or self._gui.node_has_check_box():
            pass

    def _add_shader_node_file(self):
        """node_shader_*.c"""
        pass

    def _add_node_register(self):
        """NOD_shader.h"""
        pass

    def _add_cycles_class(self):
        """nodes.h"""
        pass

    def _add_cycles_class_instance(self):
        """blender_shader.cpp"""
        pass

    def _add_cycles_node(self):
        """nodes.cpp"""
        pass

    def _add_to_node_menu(self):
        """nodeitems_builtins.py"""
        pass

    def _add_osl_shader(self):
        """"""
        node_name_underscored = self._gui.get_node_name().replace(" ", "_").lower()
        with open("/".join((self._gui.get_source_path(), "intern", "cycles", "kernel", "shaders", "node_" + node_name_underscored)), "w+") as f:
            f.write()

    def _add_kvm_shader(self):
        """"""
        pass

    def _add_glsl_shader(self):
        """"""
        pass

    def generate_node(self):
        self._add_node_definition()
