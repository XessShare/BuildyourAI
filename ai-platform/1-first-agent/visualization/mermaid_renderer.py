"""
Mermaid Renderer
Rendert Mermaid-Diagramme zu SVG/PNG mit Fallback-Mechanismen
"""

import subprocess
import re
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
import logging
import tempfile
import os

logger = logging.getLogger(__name__)


class MermaidRenderer:
    """
    Rendert Mermaid-Diagramme zu SVG/PNG
    
    Unterstützt:
    - mermaid-cli (mmdc) via npm
    - Python-Bibliothek mermaid-py (falls verfügbar)
    - Online-Rendering-Service als Fallback
    """

    def __init__(self):
        self.mmdc_path = self._find_mmdc()
        self.use_online_fallback = True

    def _find_mmdc(self) -> Optional[str]:
        """Findet mermaid-cli Installation"""
        # Prüfe ob mmdc im PATH ist
        mmdc = shutil.which("mmdc")
        if mmdc:
            return mmdc
        
        # Prüfe ob npx verfügbar ist (kann mmdc ausführen)
        npx = shutil.which("npx")
        if npx:
            return "npx"
        
        return None

    def validate_syntax(self, mermaid_code: str) -> Dict[str, Any]:
        """
        Validiert Mermaid-Syntax
        
        Args:
            mermaid_code: Mermaid-Diagramm-Code
            
        Returns:
            Dict mit 'valid' (bool) und 'error' (Optional[str])
        """
        # Basis-Validierung: Prüfe auf häufige Syntax-Fehler
        errors = []
        
        # Prüfe auf ungeschlossene Blöcke
        if mermaid_code.count('{') != mermaid_code.count('}'):
            errors.append("Ungeschlossene geschweifte Klammern")
        
        if mermaid_code.count('[') != mermaid_code.count(']'):
            errors.append("Ungeschlossene eckige Klammern")
        
        # Prüfe auf gültige Diagramm-Typen
        valid_types = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
                      'stateDiagram', 'erDiagram', 'gantt', 'pie', 'gitgraph']
        diagram_type = None
        for dt in valid_types:
            if mermaid_code.strip().startswith(dt):
                diagram_type = dt
                break
        
        if not diagram_type:
            errors.append("Kein gültiger Diagramm-Typ gefunden")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "diagram_type": diagram_type
        }

    def render_to_svg(self, mermaid_code: str, output_path: Path) -> Dict[str, Any]:
        """
        Rendert Mermaid-Diagramm zu SVG
        
        Args:
            mermaid_code: Mermaid-Diagramm-Code
            output_path: Pfad für SVG-Ausgabe
            
        Returns:
            Dict mit 'success' (bool), 'output_path' (Optional[Path]), 'error' (Optional[str])
        """
        # Validiere Syntax
        validation = self.validate_syntax(mermaid_code)
        if not validation["valid"]:
            return {
                "success": False,
                "error": f"Syntax-Fehler: {', '.join(validation['errors'])}"
            }

        # Versuche mermaid-cli
        if self.mmdc_path:
            result = self._render_with_mmdc(mermaid_code, output_path, format="svg")
            if result["success"]:
                return result

        # Versuche Online-Fallback
        if self.use_online_fallback:
            result = self._render_with_online_service(mermaid_code, output_path, format="svg")
            if result["success"]:
                return result

        return {
            "success": False,
            "error": "Keine verfügbare Rendering-Methode gefunden"
        }

    def render_to_png(self, mermaid_code: str, output_path: Path, width: int = 1920) -> Dict[str, Any]:
        """
        Rendert Mermaid-Diagramm zu PNG
        
        Args:
            mermaid_code: Mermaid-Diagramm-Code
            output_path: Pfad für PNG-Ausgabe
            width: Breite in Pixeln
            
        Returns:
            Dict mit 'success' (bool), 'output_path' (Optional[Path]), 'error' (Optional[str])
        """
        # Validiere Syntax
        validation = self.validate_syntax(mermaid_code)
        if not validation["valid"]:
            return {
                "success": False,
                "error": f"Syntax-Fehler: {', '.join(validation['errors'])}"
            }

        # Versuche mermaid-cli
        if self.mmdc_path:
            result = self._render_with_mmdc(mermaid_code, output_path, format="png", width=width)
            if result["success"]:
                return result

        # Versuche Online-Fallback (SVG zu PNG konvertieren)
        if self.use_online_fallback:
            svg_path = output_path.with_suffix('.svg')
            result = self._render_with_online_service(mermaid_code, svg_path, format="svg")
            if result["success"]:
                # Konvertiere SVG zu PNG (benötigt zusätzliche Tools)
                png_result = self._convert_svg_to_png(svg_path, output_path, width)
                if png_result["success"]:
                    return png_result

        return {
            "success": False,
            "error": "Keine verfügbare Rendering-Methode für PNG gefunden"
        }

    def _render_with_mmdc(self, mermaid_code: str, output_path: Path, format: str = "svg", width: int = 1920) -> Dict[str, Any]:
        """Rendert mit mermaid-cli (mmdc)"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as tmp_file:
                tmp_file.write(mermaid_code)
                tmp_input = tmp_file.name

            output_path.parent.mkdir(parents=True, exist_ok=True)

            cmd = [self.mmdc_path]
            if self.mmdc_path == "npx":
                cmd.append("mmdc")
            
            cmd.extend([
                "-i", tmp_input,
                "-o", str(output_path),
                "-w", str(width)
            ])

            if format == "png":
                cmd.extend(["-b", "transparent"])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            os.unlink(tmp_input)

            if result.returncode == 0 and output_path.exists():
                return {
                    "success": True,
                    "output_path": output_path,
                    "method": "mmdc"
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr or "Unbekannter Fehler"
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout beim Rendering"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _render_with_online_service(self, mermaid_code: str, output_path: Path, format: str = "svg") -> Dict[str, Any]:
        """
        Rendert mit Online-Service (mermaid.ink)
        
        Fallback-Methode wenn lokale Tools nicht verfügbar sind
        """
        try:
            import base64
            import urllib.request

            # Encode Mermaid-Code als Base64 für mermaid.ink
            mermaid_bytes = mermaid_code.encode('utf-8')
            encoded = base64.urlsafe_b64encode(mermaid_bytes).decode('utf-8')
            url = f"https://mermaid.ink/img/{encoded}"

            # Lade SVG (mermaid.ink gibt PNG zurück, daher verwenden wir einen alternativen Service)
            # Alternative: Nutze mermaid.live API
            try:
                import json
                import urllib.parse
                
                # Versuche mermaid.live API (POST)
                api_url = "https://mermaid.live/api/v1/svg"
                data = json.dumps({"code": mermaid_code}).encode('utf-8')
                
                req = urllib.request.Request(
                    api_url,
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    svg_data = response.read()
                
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(svg_data)
                
                return {
                    "success": True,
                    "output_path": output_path,
                    "method": "online_service"
                }
            except Exception as api_error:
                logger.debug(f"mermaid.live API fehlgeschlagen: {api_error}")
                
                # Fallback: Nutze mermaid.ink mit korrektem Format
                # mermaid.ink benötigt Base64-encoded Diagramm
                encoded = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
                url = f"https://mermaid.ink/svg/{encoded}"
                
                with urllib.request.urlopen(url, timeout=10) as response:
                    svg_data = response.read()
                
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(svg_data)
                
                return {
                    "success": True,
                    "output_path": output_path,
                    "method": "online_service"
                }

        except Exception as e:
            logger.warning(f"Online-Rendering fehlgeschlagen: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _convert_svg_to_png(self, svg_path: Path, png_path: Path, width: int = 1920) -> Dict[str, Any]:
        """
        Konvertiert SVG zu PNG
        
        Nutzt verschiedene Tools (cairosvg, inkscape, etc.)
        """
        # Versuche cairosvg (Python-Bibliothek)
        try:
            import cairosvg
            cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=width)
            return {
                "success": True,
                "output_path": png_path,
                "method": "cairosvg"
            }
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"cairosvg Konvertierung fehlgeschlagen: {e}")

        # Versuche inkscape
        inkscape = shutil.which("inkscape")
        if inkscape:
            try:
                result = subprocess.run(
                    [inkscape, str(svg_path), "--export-filename", str(png_path), 
                     f"--export-width={width}"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0 and png_path.exists():
                    return {
                        "success": True,
                        "output_path": png_path,
                        "method": "inkscape"
                    }
            except Exception as e:
                logger.warning(f"inkscape Konvertierung fehlgeschlagen: {e}")

        return {
            "success": False,
            "error": "Keine verfügbare SVG-zu-PNG Konvertierung"
        }

