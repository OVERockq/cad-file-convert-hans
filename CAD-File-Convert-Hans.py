import os
import subprocess
import configparser
import ezdxf
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from tqdm import tqdm
import tempfile
import shutil

# 설정 파일 경로
CONFIG_PATH = 'config.ini'

# 설정 파일에서 설정을 불러오는 함수
def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    
    settings = {
        'ODAFileConverter_Dir': config.get('Settings', 'ODAFileConverter_Dir', fallback=r"C:\Program Files\ODA\ODAFileConverter 25.8.0\ODAFileConverter.exe"),
        'DATA_DIR': config.get('Settings', 'DATA_DIR', fallback='DATA'),
        'background_color': config.get('Settings', 'background_color', fallback='white'),
        'format_choice': config.get('Settings', 'format_choice', fallback='PNG'),
        'Scale': config.getfloat('Settings', 'Scale', fallback=1.0),
        'LineWidthScale': config.getfloat('Settings', 'LineWidthScale', fallback=1.0),
        'TextScale': config.getfloat('Settings', 'TextScale', fallback=1.0),
        'text_choice': config.get('Settings', 'text_choice', fallback='1')
    }
    return settings

def change_font_to_malgun(doc):
    malgun_font = "Malgun Gothic"
    for entity in doc.modelspace().query('TEXT MTEXT'):
        if hasattr(entity.dxf, 'style'):
            entity.dxf.style = malgun_font
    if malgun_font not in doc.styles:
        doc.styles.new(malgun_font, dxfattribs={'font': "malgun.ttf"})

def set_korean_font():
    font_path = r"C:\Windows\Fonts\malgun.ttf"
    if os.path.exists(font_path):
        font_prop = FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False
        return font_prop
    return None

class CustomFrontend(Frontend):
    def __init__(self, ctx, out, text_scale, line_width_scale, font_prop):
        super().__init__(ctx, out)
        self.text_scale = text_scale
        self.line_width_scale = line_width_scale
        self.font_prop = font_prop or FontProperties(family="Malgun Gothic")

    def draw_text(self, entity, properties):
        properties.height *= self.text_scale
        if self.font_prop:
            properties.font = self.font_prop.get_name()
        super().draw_text(entity, properties)

def clear_screen():
    # 화면을 클리어하는 함수
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title():
    title = "CAD File Convert-Hans ver. 0.4"
    subtitle = "locustk@gmail.com / https://make1solve.tistory.com"
    print("\n" + title.center(50, ' ') + "\n" + subtitle.center(50, ' '))
    print("=" * 50)

def convert_dwg_to_dxf(input_path, output_folder, converter_path):
    print(f"Converting {input_path} to DXF format...")
    cmd = f'"{converter_path}" "{os.path.dirname(input_path)}" "{output_folder}" "ACAD2018" "DXF" "{0}" "{1}" "*.DWG"'
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("Conversion successful.")
    except subprocess.CalledProcessError as e:
        print(f"Conversion error: {e}")

def convert_dxf_to_output(file_path, output_format, scale, line_width_scale, text_scale, include_text, background_color):
    base_name, _ = os.path.splitext(file_path)
    output_file = f"{base_name}_with_text_x{scale}.{output_format.lower()}" if include_text else f"{base_name}_without_text_x{scale}.{output_format.lower()}"
    
    try:
        doc = ezdxf.readfile(file_path)
        change_font_to_malgun(doc)
        
        msp = doc.modelspace()
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor(background_color)
        korean_font = set_korean_font()
        
        render_context = RenderContext(doc)
        backend = MatplotlibBackend(ax)
        frontend = CustomFrontend(render_context, backend, text_scale, line_width_scale, korean_font)
        
        def entity_filter(entity):
            return include_text or entity.dxftype() not in ['TEXT', 'MTEXT']
        
        frontend.draw_layout(msp, finalize=True, filter_func=entity_filter)
        
        ax.set_axis_off()
        fig.set_size_inches(fig.get_size_inches() * scale)
        
        if output_format == 'PNG':
            fig.savefig(output_file, format="png", dpi=300, facecolor=background_color)
        elif output_format == 'PDF':
            fig.savefig(output_file, format="pdf", facecolor=background_color)
        
        plt.close(fig)
        print(f"Converted {file_path} -> {output_file}")
        
    except Exception as e:
        print(f"Error converting {file_path}: {e}")

def main():
    settings = load_config()
    
    data_folder = settings['DATA_DIR']
    converter_path = settings['ODAFileConverter_Dir']
    
    # Step 1: DWG to DXF conversion
    dwg_files = []
    for root, _, files in os.walk(data_folder):
        for file in files:
            if file.lower().endswith('.dwg'):
                dwg_files.append(os.path.join(root, file))
    
    clear_screen()
    print_title()
    
    print(f"Found {len(dwg_files)} DWG files for conversion.")
    
    total_files = len(dwg_files)
    progress_bar = tqdm(total=total_files, desc="Overall Progress", position=0)
    
    for file_path in dwg_files:
        print("\n" + "=" * 50)
        print(f"Converting {file_path}...")
        
        # Create temporary directory for the current DWG file
        with tempfile.TemporaryDirectory() as temp_folder:
            # Copy the DWG file to the temporary folder
            temp_dwg_path = os.path.join(temp_folder, os.path.basename(file_path))
            shutil.copy2(file_path, temp_dwg_path)
            
            # Convert the DWG to DXF
            convert_dwg_to_dxf(temp_dwg_path, os.path.dirname(file_path), converter_path)
        
        progress_bar.update(1)
    
    progress_bar.close()
    
    # Step 2: Find newly created DXF files and convert to output formats
    dxf_files = []
    for root, _, files in os.walk(data_folder):
        for file in files:
            if file.lower().endswith('.dxf'):
                dxf_files.append(os.path.join(root, file))
    
    print(f"Found {len(dxf_files)} DXF files for output conversion.")
    
    total_dxf_files = len(dxf_files)
    progress_bar = tqdm(total=total_dxf_files, desc="Output Conversion Progress", position=0)
    
    for file_path in dxf_files:
        current_file_message = f"Converting {file_path}..."
        print("\n" + "=" * 50)
        print(current_file_message)
        
        include_text = settings['text_choice'] in ['1', '3']
        current_step_progress = tqdm(total=2 if settings['text_choice'] == '3' else 1, desc="Current Step Progress", position=1)
        
        convert_dxf_to_output(file_path, settings['format_choice'], settings['Scale'], settings['LineWidthScale'], settings['TextScale'], include_text, background_color=settings['background_color'])
        current_step_progress.update(1)
        
        if settings['text_choice'] == '3':
            convert_dxf_to_output(file_path, settings['format_choice'], settings['Scale'], settings['LineWidthScale'], settings['TextScale'], include_text=False, background_color=settings['background_color'])
            current_step_progress.update(1)
        
        current_step_progress.close()
        progress_bar.update(1)
    
    progress_bar.close()
    print("All conversions are complete.")

if __name__ == "__main__":
    main()
