from dataclasses import dataclass
from typing import List, Optional
import xml.etree.ElementTree as ET


@dataclass
class FileChange:
    """Represents a single file change operation"""
    file_summary: str
    file_operation: str
    file_path: str
    file_code: Optional[str] = None


def parse_xml_string(xml_string: str) -> List[FileChange]:
    """Parse XML string containing file changes"""
    try:
        # Parse the XML string
        root = ET.fromstring(xml_string)
        
        # The root itself might be changed_files, or it might be inside a root
        changed_files = root if root.tag == 'changed_files' else root.find('changed_files')
        if changed_files is None:
            raise ValueError("No <changed_files> element found in XML")
        
        changes = []
        # Process each file element
        for file_elem in changed_files.findall('file'):
            # Extract required elements
            summary = file_elem.findtext('file_summary', '').strip()
            operation = file_elem.findtext('file_operation', '').strip()
            path = file_elem.findtext('file_path', '').strip()
            
            # Get optional code content
            code_elem = file_elem.find('file_code')
            code = code_elem.text.strip() if code_elem is not None and code_elem.text else ''
            
            if not operation or not path:
                continue
                
            changes.append(FileChange(
                file_summary=summary,
                file_operation=operation,
                file_path=path,
                file_code=code
            ))
            
        return changes
        
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML format: {e}")
    except Exception as e:
        raise ValueError(f"Error parsing XML: {e}")
