<template>
  <div class="import-component">
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Procesando...</p>
    </div>

    <Transition name="fade" mode="out-in">
      
      <div v-if="step === 'initial'" key="initial" class="step-container">
        <div class="drop-zone" @click="openFilePicker" @dragover.prevent @drop.prevent="handleDrop" @dragenter.prevent @dragleave.prevent>
          <input type="file" @change="handleFileChange" accept=".xlsx, .xls" ref="fileInput" class="hidden">
          <svg class="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          <p class="font-semibold text-gray-700">Haz clic para seleccionar un archivo</p>
          <p class="text-sm text-gray-500">o arrástralo aquí (Excel: .xlsx, .xls)</p>
        </div>
      </div>

      <div v-else-if="step === 'mapping'" key="mapping" class="step-container">
        <h5 class="step-title">Mapeo de Columnas</h5>
        <p class="step-description">Asocia las columnas de tu Excel con los campos de la base de datos.</p>
        
        <div class="mapping-sheets" v-if="sheetNames.length > 0">
          <p class="font-bold">Hojas Leídas y Fusionadas:</p>
          <span v-for="sheet in sheetNames" :key="sheet" class="sheet-tag">{{ sheet }}</span>
        </div>

        <div class="mapping-fields grid grid-cols-2 gap-4 mt-4">
          
          <h6 class="col-span-2 mt-2 font-bold text-lg text-teal-700">Datos Principales (Requerido)</h6>
          
          <div class="field-map required">
            <label for="map-nombre">Nombre del Producto</label>
            <select id="map-nombre" v-model="columnMap.nombre" required>
              <option disabled value="">Selecciona una columna...</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>
          <div class="field-map required">
            <label for="map-stock">Stock Actual</label>
            <select id="map-stock" v-model="columnMap.stock_actual" required>
              <option disabled value="">Selecciona una columna...</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>

          <div class="field-map">
            <label for="map-categoria">Categoría (Opcional)</label>
            <select id="map-categoria" v-model="columnMap.categoria">
              <option value="">(Opcional)</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>
          <div class="field-map">
            <label for="map-unidad">Unidad de Medida (Opcional)</label>
            <select id="map-unidad" v-model="columnMap.unidad_medida">
              <option value="">(Opcional)</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>

          <h6 class="col-span-2 mt-4 font-bold text-lg text-indigo-700">Datos Transaccionales (Opcional)</h6>

          <div class="field-map">
            <label for="map-compra">Cantidad Comprada</label>
            <select id="map-compra" v-model="columnMap.cantidad_comprada">
              <option value="">(Opcional)</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>
          <div class="field-map">
            <label for="map-venta">Cantidad Vendida</label>
            <select id="map-venta" v-model="columnMap.cantidad_vendida">
              <option value="">(Opcional)</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>
          
          <div class="field-map">
            <label for="map-proveedor">Nombre del Proveedor</label>
            <select id="map-proveedor" v-model="columnMap.proveedor">
              <option value="">(Opcional)</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>
          <div class="field-map">
            <label for="map-fecha-pedido">Fecha de Pedido</label>
            <select id="map-fecha-pedido" v-model="columnMap.fecha_pedido">
              <option value="">(Opcional)</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>
          <div class="field-map">
            <label for="map-fecha-recepcion">Fecha de Recepción</label>
            <select id="map-fecha-recepcion" v-model="columnMap.fecha_recepcion">
              <option value="">(Opcional)</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>
        </div>

        <div class="action-buttons mt-6">
          <button @click="goToPreview" class="btn btn-primary" :disabled="!columnMap.nombre || !columnMap.stock_actual">Continuar a Previsualización</button>
          <button @click="resetFlow()" class="btn btn-secondary">Cancelar</button>
        </div>
      </div>

      <div v-else-if="step === 'preview'" key="preview" class="step-container">
        <h5 class="step-title">Previsualiza y Confirma</h5>
        <p class="step-description">Se procesarán {{ processedData.length }} filas. Revisa que los datos se hayan interpretado correctamente. Solo se muestran las primeras 5 filas.</p>
        
        <div class="table-responsive">
          <table class="preview-table">
            <thead>
              <tr>
                <th v-for="header in previewHeaders" :key="header">{{ header }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in processedData.slice(0, 5)" :key="index">
                <td v-for="header in previewHeaders" :key="header">
                  {{ row[header] !== null && row[header] !== undefined ? row[header] : '-' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="action-buttons mt-6">
          <button @click="submitFile" class="btn btn-primary">Confirmar e Importar</button>
          <button @click="step = 'mapping'" class="btn btn-secondary">Corregir Mapeo</button>
        </div>
      </div>
      
      <div v-else-if="step === 'success'" key="success" class="step-container text-center">
        <h5 class="text-2xl font-bold text-green-600 mb-4">🎉 ¡Importación Exitosa!</h5>
        <p class="text-gray-700">{{ successMessage }}</p>
        <button @click="resetFlow()" class="btn btn-primary mt-6">Volver al Inicio</button>
      </div>

    </Transition>
    
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import * as XLSX from 'xlsx';
import axios from '@/api/axios.js';
import { useAuthStore } from '@/stores/auth.js';

const authStore = useAuthStore();

const emit = defineEmits(['upload-success']);
const step = ref('initial');
const selectedFile = ref(null);
const fileInput = ref(null);
const error = ref('');
const loading = ref(false);
const csvHeaders = ref([]);
const originalData = ref([]);
const sheetNames = ref([]);
const successMessage = ref('');

const columnMap = ref({
  nombre: '',
  stock_actual: '',
  categoria: '',
  unidad_medida: '',
  cantidad_comprada: '',
  cantidad_vendida: '',
  proveedor: '',
  fecha_pedido: '',
  fecha_recepcion: ''
});

const aliasMap = {
  nombre: ['producto', 'nombre', 'item', 'articulo', 'descripción', 'descripcion', 'código', 'codigo', 'sku', 'name'],
  stock_actual: ['stock', 'stock_actual', 'en_stock', 'cantidad', 'unidades', 'disponible', 'existencia', 'inventory', 'available', 'stock_minimo'],
  categoria: ['categoría', 'categoria', 'tipo', 'familia', 'grupo', 'linea', 'department', 'category'],
  unidad_medida: ['unidad', 'medida', 'unidad_medida', 'uom', 'unidad de medida'],
  cantidad_comprada: ['comprada', 'cant_compra', 'cantidad_compra', 'entradas', 'recepción', 'recibido', 'compras', 'bought', 'inbound', 'cantidad_comprada'],
  cantidad_vendida: ['vendida', 'cant_venta', 'cantidad_venta', 'salidas', 'despachado', 'ventas', 'sold', 'outbound', 'cantidad_vendida'],
  proveedor: ['proveedor', 'suplidor', 'supplier', 'vendor', 'vendedor'],
  fecha_pedido: ['fecha_pedido', 'f_pedido', 'fecha_orden', 'order_date', 'fecha_compra'],
  fecha_recepcion: ['fecha_recepcion', 'f_recepcion', 'recibo', 'delivery_date', 'fecha recibida', 'fecha_recepcion'],
};

// --- Funciones de Normalización y Detección ---

const normalizeHeader = (header) => {
    return String(header || '').toLowerCase().trim().replace(/\s+/g, '_').replace(/-/g, '_').replace(/[^\w]/gi, '');
};

const findProductColumn = (headers) => {
    const normalizedHeaders = headers.map(h => normalizeHeader(h));
    const normalizedAliases = aliasMap.nombre.map(a => a.replace(/\s+/g, '_'));

    // Prioridad 1: Buscar una coincidencia exacta.
    for (let i = 0; i < normalizedHeaders.length; i++) {
        if (normalizedAliases.includes(normalizedHeaders[i])) {
            return { index: i, original: headers[i] };
        }
    }

    // Prioridad 2 (Respaldo): Si no hay coincidencias exactas, buscar por inclusión.
    for (let i = 0; i < normalizedHeaders.length; i++) {
        if (normalizedAliases.some(alias => normalizedHeaders[i].includes(alias))) {
            return { index: i, original: headers[i] };
        }
    }
    
    return null;
};

const classifySheetType = (headers, sheetName = '') => {
    const nameLower = sheetName.toLowerCase();
    if (nameLower.includes('venta') || nameLower.includes('sale')) return 'ventas';
    if (nameLower.includes('compra') || nameLower.includes('purchase') || nameLower.includes('orden')) return 'compras';
    
    const normalized = headers.map(h => normalizeHeader(h));
    const hasStock = aliasMap.stock_actual.some(alias => normalized.some(h => h === alias.replace(/\s+/g, '_')));
    if (hasStock) return 'master';

    const hasVentaExact = normalized.includes('cantidad_vendida') || headers.some(h => h.toLowerCase() === 'cantidad_vendida');
    if (hasVentaExact) return 'ventas';

    const hasCompraExact = normalized.includes('cantidad_comprada') || headers.some(h => h.toLowerCase() === 'cantidad_comprada');
    const hasProveedor = aliasMap.proveedor.some(alias => normalized.some(h => h.includes(alias.replace(/\s+/g, '_'))));
    if (hasCompraExact || hasProveedor) return 'compras';
    
    return 'unknown';
};

const findMasterSheetInfo = (workbook) => {
    for (const sheetName of workbook.SheetNames) {
        const nameLower = sheetName.toLowerCase();
        if (nameLower.includes('master') || nameLower.includes('principal') || nameLower.includes('inventario') || nameLower.includes('productos') || nameLower.includes('ventas_actuales')) {
            const ws = workbook.Sheets[sheetName];
            if (!ws || !ws['!ref']) continue;
            const data = XLSX.utils.sheet_to_json(ws, { defval: null, header: 1 });
            if (!data.length) continue;
            const headers = data[0].map(h => String(h || ''));
            return { name: sheetName, headers, type: 'master' };
        }
    }
    
    for (const sheetName of workbook.SheetNames) {
        const ws = workbook.Sheets[sheetName];
        if (!ws || !ws['!ref']) continue;
        const data = XLSX.utils.sheet_to_json(ws, { defval: null, header: 1 });
        if (!data.length) continue;
        const headers = data[0].map(h => String(h || ''));
        const type = classifySheetType(headers, sheetName);
        if (type === 'master') {
            return { name: sheetName, headers, type };
        }
    }
    
    const sheetsInfo = workbook.SheetNames.map(name => {
        const ws = workbook.Sheets[name];
        if (!ws || !ws['!ref']) return null;
        const data = XLSX.utils.sheet_to_json(ws, { defval: null, header: 1 });
        if (!data.length) return null;
        const headers = data[0].map(h => String(h || ''));
        const productCol = findProductColumn(headers);
        return productCol ? { name, headers, columnCount: headers.length } : null;
    }).filter(Boolean);
    
    sheetsInfo.sort((a, b) => b.columnCount - a.columnCount);
    return sheetsInfo[0] ? { name: sheetsInfo[0].name, headers: sheetsInfo[0].headers, type: 'master' } : null;
};

const processMasterSheet = (workbook, masterSheetName, allHeaders) => {
    const productDataMap = new Map();
    const worksheet = workbook.Sheets[masterSheetName];
    const data = XLSX.utils.sheet_to_json(worksheet, { defval: null, header: 1 });
    if (data.length < 2) return productDataMap;
    
    const headers = data[0].map(h => String(h || ''));
    const productCol = findProductColumn(headers);
    if (!productCol) return productDataMap;
    
    headers.forEach(h => h && allHeaders.add(h));
    
    for (let i = 1; i < data.length; i++) {
        const row = data[i];
        const productName = String(row[productCol.index] || '').trim();
        if (!productName) continue;
        
        const rowData = { _source: 'master' };
        headers.forEach((header, idx) => {
            if (header && row[idx] !== undefined && row[idx] !== null && row[idx] !== '') {
                rowData[header] = row[idx];
            }
        });
        productDataMap.set(productName, rowData);
    }
    return productDataMap;
};

const aggregateTransactionalData = (data, productColIndex, headers, aggregationFields) => {
    const aggregated = {};
    for (let i = 1; i < data.length; i++) {
        const row = data[i];
        const productName = String(row[productColIndex] || '').trim();
        if (!productName) continue;
        
        const normalizedProductName = productName.toLowerCase().replace(/\s+/g, ' ').trim();
        if (!aggregated[normalizedProductName]) {
            aggregated[normalizedProductName] = { _originalName: productName };
            headers.forEach((header, idx) => {
                if (header && row[idx] !== undefined && row[idx] !== null && row[idx] !== '') {
                    aggregated[normalizedProductName][header] = row[idx];
                }
            });
        } else {
            headers.forEach((header, idx) => {
                if (!header) return;
                const normalized = normalizeHeader(header);
                const isAggregatable = aggregationFields.some(field => normalized.includes(field));
                if (isAggregatable && row[idx] !== undefined && row[idx] !== null && row[idx] !== '') {
                    const currentVal = parseFloat(String(aggregated[normalizedProductName][header] || 0).replace(/[$,]/g, ''));
                    const newVal = parseFloat(String(row[idx]).replace(/[$,]/g, ''));
                    if (!isNaN(newVal)) {
                        aggregated[normalizedProductName][header] = (isNaN(currentVal) ? 0 : currentVal) + newVal;
                    }
                } else if (!aggregated[normalizedProductName][header] && row[idx] !== undefined && row[idx] !== null && row[idx] !== '') {
                    aggregated[normalizedProductName][header] = row[idx];
                }
            });
        }
    }
    return aggregated;
};

const mergeTransactionalData = (workbook, productDataMap, allHeaders, masterSheetName) => {
    workbook.SheetNames.forEach(sheetName => {
        if (sheetName === masterSheetName) return;
        
        const worksheet = workbook.Sheets[sheetName];
        const data = XLSX.utils.sheet_to_json(worksheet, { defval: null, header: 1 });
        if (data.length < 2) return;
        
        const headers = data[0].map(h => String(h || ''));
        const productCol = findProductColumn(headers);
        if (!productCol) return;
        
        const sheetType = classifySheetType(headers, sheetName);
        let aggregationFields, consolidatedFieldName;
        if (sheetType === 'ventas') {
            aggregationFields = ['vendida', 'venta', 'salida'];
            consolidatedFieldName = 'cantidad_vendida';
        } else {
            aggregationFields = ['comprada', 'compra', 'entrada', 'recibida'];
            consolidatedFieldName = 'cantidad_comprada';
        }
        
        headers.forEach(h => h && allHeaders.add(h));
        const aggregated = aggregateTransactionalData(data, productCol.index, headers, aggregationFields);
        
        let quantityColName = null;
        for (const header of headers) {
            const normalized = normalizeHeader(header);
            if (sheetType === 'ventas' && (normalized === 'cantidad_vendida' || normalized === 'vendida')) {
                quantityColName = header; break;
            }
            if (sheetType === 'compras' && (normalized === 'cantidad_comprada' || normalized === 'comprada')) {
                quantityColName = header; break;
            }
        }
        if (!quantityColName) {
            for (const header of headers) {
                const normalized = normalizeHeader(header);
                if (aggregationFields.some(field => normalized.includes(field))) {
                    quantityColName = header; break;
                }
            }
        }
        
        Object.keys(aggregated).forEach(normalizedProductName => {
            const productData = aggregated[normalizedProductName];
            const originalName = productData._originalName;
            
            let matchingProduct = null;
            for (const [key, value] of productDataMap.entries()) {
                const normalizedKey = key.toLowerCase().replace(/\s+/g, ' ').trim();
                if (normalizedKey === normalizedProductName || key === originalName) {
                    matchingProduct = value; break;
                }
            }
            
            if (matchingProduct) {
                if (quantityColName && productData[quantityColName] !== undefined) {
                    const currentValue = matchingProduct[consolidatedFieldName] || 0;
                    const newValue = parseFloat(String(productData[quantityColName]).replace(/[$,]/g, '')) || 0;
                    matchingProduct[consolidatedFieldName] = currentValue + newValue;
                }
                
                Object.keys(productData).forEach(header => {
                    if (header !== quantityColName && header !== '_originalName' && (!matchingProduct[header] || matchingProduct[header] === null || matchingProduct[header] === '')) {
                        matchingProduct[header] = productData[header];
                    }
                });
            }
        });
    });
};

const guessColumnMappings = (headers) => {
  const newMap = {};
  Object.keys(columnMap.value).forEach(key => newMap[key] = '');
  headers.forEach(header => {
    const normalizedHeader = normalizeHeader(header);
    for (const key in aliasMap) {
      if (aliasMap[key].includes(normalizedHeader) && !newMap[key]) {
        newMap[key] = header;
      }
    }
  });
  if (!newMap.cantidad_vendida && headers.includes('cantidad_vendida')) newMap.cantidad_vendida = 'cantidad_vendida';
  if (!newMap.cantidad_comprada && headers.includes('cantidad_comprada')) newMap.cantidad_comprada = 'cantidad_comprada';
  columnMap.value = newMap;
};

const parseDate = (value) => {
    if (!value) return null;
    if (typeof value === 'number') {
        const date = XLSX.SSF.parse_date_code(value);
        if (date.y < 1900) return null;
        const d = new Date(date.y, date.m - 1, date.d, date.H, date.M, date.S);
        return d.toISOString().split('T')[0];
    }
    if (value instanceof Date && !isNaN(value)) return value.toISOString().split('T')[0];
    if (typeof value === 'string') {
        const formattedString = value.replace(/(\d{2})[-/](\d{2})[-/](\d{4})/, '$3-$2-$1');
        const d = new Date(formattedString);
        if (!isNaN(d.getTime())) return d.toISOString().split('T')[0];
    }
    return value;
};

// NUEVA PROPIEDAD COMPUTADA para los encabezados de la previsualización
const previewHeaders = computed(() => {
  if (!processedData.value || processedData.value.length === 0) {
    return [];
  }
  // Crea los encabezados a partir de las claves del primer objeto de datos
  return Object.keys(processedData.value[0]);
});

// PROPIEDAD COMPUTADA ACTUALIZADA con la corrección para leer cantidades
const processedData = computed(() => {
  if (!originalData.value.length || !columnMap.value.nombre || !columnMap.value.stock_actual) return [];
  
  return originalData.value.map(row => {
    const data = {};
    for (const key in columnMap.value) {
      let colName = columnMap.value[key];

      // Para nuestros campos consolidados, ignoramos el mapeo y usamos la clave directa
      if (key === 'cantidad_vendida' || key === 'cantidad_comprada') {
        colName = key;
      }

      if (colName && row[colName] !== undefined && row[colName] !== null && row[colName] !== '') {
        let value = row[colName];
        if (key.includes('fecha')) {
          data[key] = parseDate(value);
        } else if (key.includes('cantidad') || key.includes('stock')) {
          const num = parseFloat(String(value).replace(/[$,]/g, '').trim());
          data[key] = isNaN(num) ? 0 : num;
        } else {
          data[key] = String(value).trim();
        }
      } else {
        if (key.includes('cantidad')) data[key] = 0;
        else if (key.includes('stock')) data[key] = colName ? 0 : null;
        else if (key.includes('fecha')) data[key] = null;
        else data[key] = '';
      }
    }
    if (!data.nombre || data.stock_actual === null) return null;
    return data;
  }).filter(row => row !== null);
});

const processExcelFile = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const workbook = XLSX.read(new Uint8Array(e.target.result), { type: 'array', cellDates: true });
                if (!workbook.SheetNames || workbook.SheetNames.length === 0) return reject(new Error("El archivo no contiene hojas."));
                
                const masterSheetInfo = findMasterSheetInfo(workbook);
                if (!masterSheetInfo) return reject(new Error("No se pudo identificar una hoja principal. Asegúrate de que una hoja contenga una columna de 'producto' o de 'stock'."));
                
                const allHeaders = new Set();
                const productDataMap = processMasterSheet(workbook, masterSheetInfo.name, allHeaders);
                if (productDataMap.size === 0) return reject(new Error("No se encontraron productos en la hoja principal."));
                
                mergeTransactionalData(workbook, productDataMap, allHeaders, masterSheetInfo.name);
                
                resolve({
                    data: Array.from(productDataMap.values()),
                    headers: Array.from(allHeaders).filter(h => h),
                    sheetNames: workbook.SheetNames
                });
            } catch (err) {
                reject(new Error(`Error al procesar el archivo. Detalles: ${err.message}`));
            }
        };
        reader.onerror = () => reject(new Error('Error de lectura del archivo.'));
        reader.readAsArrayBuffer(file);
    });
};

function handleFileChange(event) { processFile(event.target.files[0]); }
function handleDrop(event) { processFile(event.dataTransfer.files[0]); }
function openFilePicker() { fileInput.value.click(); }

async function processFile(file) {
  if (!file) return;
  selectedFile.value = file;
  resetFlow(false);
  loading.value = true;
  error.value = '';
  try {
    const result = await processExcelFile(file);
    csvHeaders.value = result.headers;
    originalData.value = result.data;
    sheetNames.value = result.sheetNames;
    guessColumnMappings(csvHeaders.value);
    
    if (processedData.value.length > 0) step.value = 'preview';
    else if (columnMap.value.nombre && columnMap.value.stock_actual) step.value = 'preview'; 
    else step.value = 'mapping';
  } catch (err) {
    error.value = err.message;
    resetFlow();
  } finally {
    loading.value = false;
  }
}

function goToPreview() {
  if (!columnMap.value.nombre || !columnMap.value.stock_actual) {
    error.value = "Debes mapear el Nombre del Producto y el Stock Actual.";
    return;
  }
  error.value = '';
  step.value = 'preview';
}

async function submitFile() {
  loading.value = true;
  error.value = '';
  const empresaId = authStore.empresaId;
  if (!empresaId) {
      error.value = 'No se pudo obtener el ID de la empresa. Inicia sesión de nuevo.';
      loading.value = false;
      return;
  }
  try {
    const response = await axios.post(`/empresas/${empresaId}/importar-inventario/`, processedData.value);
    emit('upload-success', response.data.mensaje);
    successMessage.value = response.data.mensaje;
    step.value = 'success';
  } catch (err) {
    const details = err.response?.data?.detalles || (Array.isArray(err.response?.data?.error) ? err.response.data.error.join(', ') : err.response?.data?.error);
    error.value = details || 'Ocurrió un error inesperado al importar.';
  } finally {
    loading.value = false;
  }
}

function resetFlow(clearFile = true) {
  if (clearFile && fileInput.value) fileInput.value.value = null;
  step.value = 'initial';
  error.value = '';
  successMessage.value = '';
  csvHeaders.value = [];
  originalData.value = [];
  sheetNames.value = [];
  columnMap.value = {
    nombre: '', stock_actual: '', categoria: '', unidad_medida: '',
    cantidad_comprada: '', cantidad_vendida: '', proveedor: '',
    fecha_pedido: '', fecha_recepcion: ''
  };
}
</script>

<style scoped>
.import-component { background-color: #f8fafc; padding: 2.5rem; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); position: relative; overflow: hidden; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(15px); }
.step-container { width: 100%; }
.drop-zone { border: 2px dashed #e2e8f0; border-radius: 10px; padding: 3rem; text-align: center; cursor: pointer; transition: all 0.3s ease; display: flex; flex-direction: column; justify-content: center; align-items: center; }
.drop-zone:hover { border-color: #0d9488; background-color: #f0fdfa; }
.upload-icon { width: 48px; height: 48px; color: #0d9488; margin-bottom: 1rem; }
.loading-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(255, 255, 255, 0.8); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 50; }
.spinner { border: 4px solid rgba(13, 148, 136, 0.2); border-left-color: #0d9488; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.error-message { color: #ef4444; background-color: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 8px; margin-top: 1.5rem; text-align: center; }
.step-title { font-size: 1.25rem; font-weight: 600; color: #1a202c; margin-bottom: 0.5rem; }
.step-description { color: #4a5568; margin-bottom: 2rem; }
.mapping-fields { display: grid; gap: 1.5rem; margin-bottom: 2rem; }
.field-map { display: flex; flex-direction: column; }
.field-map label { font-weight: 600; margin-bottom: 0.5rem; color: #2d3748; }
.field-map select { padding: 10px; border: 1px solid #cbd5e0; border-radius: 6px; font-size: 1rem; }
.action-buttons { display: flex; gap: 1rem; margin-top: 1.5rem; }
.btn { padding: 12px 30px; border-radius: 8px; font-weight: 700; transition: all 0.2s ease; cursor: pointer; border: none; }
.btn-primary { background-color: #0d9488; color: white; }
.btn-primary:hover { background-color: #0f766e; }
.btn-primary:disabled { background-color: #94a3b8; cursor: not-allowed; }
.btn-secondary { background-color: #e2e8f0; color: #2d3748; }
.btn-secondary:hover { background-color: #cbd5e0; }
.table-responsive { overflow-x: auto; max-height: 300px; border: 1px solid #e2e8f0; border-radius: 8px; }
.preview-table { width: 100%; border-collapse: collapse; }
.preview-table th, .preview-table td { border-bottom: 1px solid #e2e8f0; padding: 12px 15px; text-align: left; white-space: nowrap;}
.preview-table th { background-color: #f8fafc; font-weight: 600; position: sticky; top: 0; }
.mapping-fields.grid-cols-2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }
.field-map.required label::after { content: ' *'; color: red; }
.sheet-tag { display: inline-block; background-color: #e0fdfa; color: #0d9488; padding: 0.25rem 0.5rem; border-radius: 0.25rem; margin-right: 0.5rem; font-size: 0.875rem; margin-top: 5px; }
.hidden { display: none; }
.mapping-sheets { margin-bottom: 1rem; }
</style>