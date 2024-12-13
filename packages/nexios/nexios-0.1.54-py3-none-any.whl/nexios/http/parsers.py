# from multipart import MultipartParser
from typing import Dict, Union, Optional
# from io import BytesIO
from urllib.parse import parse_qs

# def parse_multipart_data(body: bytes, boundary: bytes) -> Dict[str, Union[bytes, BytesIO]]:
#     form_data = {}
#     current_part = None
    
#     def on_part_begin():
#         nonlocal current_part
#         current_part = {'data': b'', 'headers': {}}
    
#     def on_header(name: bytes, value: bytes):
#         nonlocal current_part
#         current_part['headers'][name] = value
    
#     def on_data(data: bytes):
#         nonlocal current_part
#         current_part['data'] += data
    
#     def on_part_complete():
#         nonlocal current_part, form_data
#         print("Sssss")
#         if current_part:
#             headers = current_part['headers']
#             disp_header = headers.get(b'content-disposition', b'')
#             print("dsp_headers",disp_header)
#             name = None
#             filename = None
            
#             for item in disp_header.split(b';'):
#                 item = item.strip()
#                 if item.startswith(b'name='):
#                     name = item[5:].strip(b'"\'')
#                 elif item.startswith(b'filename='):
#                     filename = item[9:].strip(b'"\'')
            
#             if name:
#                 decoded_name = name.decode()
#                 if filename:
#                     form_data[decoded_name] = BytesIO(current_part['data'])
#                 else:
#                     form_data[decoded_name] = current_part['data']
    
#     parser = MultipartParser(
#         boundary=boundary,
#         callbacks={
#             'on_part_begin': on_part_begin,
#             'on_header': on_header,
#             'on_data': on_data,
#             'on_part_complete': on_part_complete
#         }
#     )
    
#     parser.write(body)
#     parser.finalize()
    
#     return form_data

def parse_urlencoded_data(body: bytes) -> Dict[str, bytes]:
    """Parse URL-encoded form data and return a dictionary of field names to values."""
    decoded = body.decode('utf-8')
    parsed = parse_qs(decoded)
    # Convert values from lists to single values since HTML forms don't typically
    # have multiple values for the same field
    return {k: v[0].encode('utf-8') for k, v in parsed.items()}

# def parse_form_data(body: bytes, content_type: bytes) -> Dict[str, Union[bytes, BytesIO]]:
#     """
#     Parse form data based on content type.
#     Supports both multipart/form-data and application/x-www-form-urlencoded.
#     """
#     content_type = content_type.split(b';')[0].strip().lower()
    
#     if content_type == b'application/x-www-form-urlencoded':
#         return parse_urlencoded_data(body)
    
#     elif content_type == b'multipart/form-data':
#         boundary = None
#         for part in content_type.split(b';'):
#             part = part.strip()
#             if part.startswith(b'boundary='):
#                 boundary = part[9:]
#                 break
#         if not boundary:
#             raise ValueError("No boundary found in multipart content type")
#         return parse_multipart_data(body, boundary)
    
#     else:
#         raise ValueError(f"Unsupported content type: {content_type.decode()}")



import cgi
from io import BytesIO
from typing import Dict,Union
def parse_multipart_data(body: bytes, boundary: bytes) -> Dict[str, Union[bytes, BytesIO]]:
    fp = BytesIO(body)
    environ = {'CONTENT_TYPE': f'multipart/form-data; boundary={boundary.decode()}'}
    form = cgi.FieldStorage(fp=fp, environ=environ, keep_blank_values=True)
    
    form_data = {}
    for key in form.keys():
        item = form[key]
        if item.filename:
            form_data[key] = BytesIO(item.file.read())  # File upload
        else:
            form_data[key] = item.value.encode('utf-8')  # Regular field
    
    return form_data
