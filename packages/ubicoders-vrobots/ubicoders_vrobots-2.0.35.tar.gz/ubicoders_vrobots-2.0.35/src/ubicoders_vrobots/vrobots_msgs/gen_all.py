from clear import clear_all
from gen_cmds_dotnet import generate_cmds_dotnet
from gen_cmds_python import gen_cmds_python
from gen_cmds_ts import generate_cmds_typescript
from gen_fid_python import gen_fid_python
from gen_states_helper import gen_states_helper
from gen_flatbuffers import compile_fb
from gen_states_enum_dotnet import gen_states_enum
from gen_states_printer_dotnet import generate_state_console_print_helper
from gen_fb_srv_defs import generate_fb_definitions
from remove_js_extension import remove_js_extension


def main():
    clear_all()
    generate_fb_definitions()
    compile_fb()
    generate_cmds_dotnet()
    gen_cmds_python()
    generate_cmds_typescript()
    gen_fid_python()
    gen_states_helper()
    gen_states_enum()
    generate_state_console_print_helper()
    remove_js_extension()


if __name__ == "__main__":
    main()
