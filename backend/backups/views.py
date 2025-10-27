from django.shortcuts import render

# Create your views here.
# views.py
import os
import json
import csv
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.db import connection
from django.core.serializers import serialize
import mysql.connector
from datetime import datetime
import zipfile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class DatabaseDumpView(View):
    template_name = 'backups/database_dump.html'
    
    def get(self, request):
        """Render the main dump interface"""
        return render(request, self.template_name)
    
    def get_database_tables(self):
        """Get list of all tables in the database"""
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]
            else:
                # For other databases, you might need different queries
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
        return tables
    
    def get_table_data(self, table_name):
        """Get all data from a specific table"""
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        
        return {
            'columns': columns,
            'rows': rows
        }
    
    def export_to_json(self, table_data, output_path):
        """Export table data to JSON file"""
        data = []
        for row in table_data['rows']:
            row_dict = {}
            for i, column in enumerate(table_data['columns']):
                # Handle different data types
                if isinstance(row[i], (datetime,)):
                    row_dict[column] = row[i].isoformat()
                else:
                    row_dict[column] = row[i]
            data.append(row_dict)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def export_to_csv(self, table_data, output_path):
        """Export table data to CSV file"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(table_data['columns'])
            for row in table_data['rows']:
                writer.writerow(row)
    
    def export_to_sql(self, table_name, table_data, output_path):
        """Export table data to SQL insert statements"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"-- Dump of table: {table_name}\n")
            f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for row in table_data['rows']:
                values = []
                for value in row:
                    if value is None:
                        values.append("NULL")
                    elif isinstance(value, (int, float)):
                        values.append(str(value))
                    else:
                        # Escape quotes and format as string
                        escaped_value = str(value).replace("'", "''")
                        values.append(f"'{escaped_value}'")
                
                columns_str = ", ".join([f"`{col}`" for col in table_data['columns']])
                values_str = ", ".join(values)
                
                f.write(f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({values_str});\n")
    
    def create_zip_file(self, files, zip_path):
        """Create a zip file containing all dump files"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files:
                zipf.write(file_path, os.path.basename(file_path))

@method_decorator(csrf_exempt, name='dispatch')
class DumpDataAPI(View):
    """API endpoint for dumping data"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            tables = data.get('tables', [])
            format_type = data.get('format', 'json')
            output_folder = data.get('output_folder', '')
            create_zip = data.get('create_zip', False)
            
            # Validate output folder
            if not output_folder:
                return JsonResponse({
                    'success': False,
                    'error': 'Output folder is required'
                })
            
            # Create output folder if it doesn't exist
            os.makedirs(output_folder, exist_ok=True)
            
            dump_view = DatabaseDumpView()
            all_tables = dump_view.get_database_tables()
            
            # If no specific tables selected, dump all tables
            if not tables:
                tables = all_tables
            
            dumped_files = []
            
            for table_name in tables:
                if table_name not in all_tables:
                    continue
                
                # Get table data
                table_data = dump_view.get_table_data(table_name)
                
                # Generate output filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{table_name}_{timestamp}.{format_type}"
                output_path = os.path.join(output_folder, filename)
                
                # Export based on format
                if format_type == 'json':
                    dump_view.export_to_json(table_data, output_path)
                elif format_type == 'csv':
                    dump_view.export_to_csv(table_data, output_path)
                elif format_type == 'sql':
                    dump_view.export_to_sql(table_name, table_data, output_path)
                
                dumped_files.append(output_path)
            
            # Create zip file if requested
            zip_path = None
            if create_zip and dumped_files:
                zip_filename = f"database_dump_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                zip_path = os.path.join(output_folder, zip_filename)
                dump_view.create_zip_file(dumped_files, zip_path)
            
            return JsonResponse({
                'success': True,
                'message': f'Successfully dumped {len(dumped_files)} tables',
                'dumped_files': [os.path.basename(f) for f in dumped_files],
                'zip_file': os.path.basename(zip_path) if zip_path else None,
                'output_folder': output_folder
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

@method_decorator(csrf_exempt, name='dispatch')
class GetTablesAPI(View):
    """API endpoint to get list of database tables"""
    
    def get(self, request):
        try:
            dump_view = DatabaseDumpView()
            tables = dump_view.get_database_tables()
            
            return JsonResponse({
                'success': True,
                'tables': tables
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

class DownloadDumpView(View):
    """View to download generated dump files"""
    
    def get(self, request):
        file_path = request.GET.get('file_path', '')
        
        if not file_path or not os.path.exists(file_path):
            return HttpResponse("File not found", status=404)
        
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response