<template>
  <section class="usuarios max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between mb-6">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-slate-800">Gestión de Usuarios</h1>
        <p class="text-slate-500">Administra los usuarios, sus roles y permisos dentro del sistema.</p>
      </div>
      <button
        class="w-full sm:w-auto px-4 py-2 rounded-md bg-teal-500 text-white font-semibold hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 shadow-sm"
        @click="openAddUser"
      >+ Agregar Nuevo Usuario</button>
    </div>

    <div class="bg-white rounded-lg shadow p-4 mb-6">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="relative">
          <input v-model.trim="search" type="text" placeholder="Buscar por nombre o correo…"
            class="w-full pl-10 pr-3 py-2 border rounded-lg focus:ring-2 focus:ring-teal-400 focus:border-teal-400" />
          <svg class="pointer-events-none absolute left-3 top-2.5 h-5 w-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
        <div>
          <select v-model="roleFilter"
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-teal-400 focus:border-teal-400 h-full">
            <option value="">Todos los roles</option>
            <option value="admin">Administrador</option>
            <option value="manager">Manager</option>
            <option value="worker">Worker</option>
            <option value="viewer">Viewer</option>
          </select>
        </div>
        <div class="flex gap-2 items-center">
          <button class="w-full sm:w-auto px-4 py-2 rounded border hover:bg-slate-50" @click="clearFilters">Limpiar</button>
          <div class="hidden sm:flex items-center text-sm text-slate-500 ml-2">
            {{ filteredUsers.length }} resultado(s)
          </div>
        </div>
      </div>
      <div class="sm:hidden text-sm text-slate-500 mt-3">
        {{ filteredUsers.length }} resultado(s)
      </div>
    </div>

    <div v-if="listForDesktop.length > 0" class="space-y-3">
        <div v-for="u in listForDesktop" :key="u.id" class="bg-white rounded-lg shadow p-4 sm:p-5">
            <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div class="flex items-center gap-4 flex-1 min-w-0">
                <div class="h-11 w-11 rounded-full flex items-center justify-center text-white font-bold shrink-0 text-base"
                        :style="{ backgroundColor: pillColor(u.role, true) }">
                    {{ initials(u.name) }}
                </div>
                <div class="min-w-0">
                    <p class="font-semibold text-slate-800 truncate">{{ u.name }}</p>
                    <p class="text-slate-500 text-sm truncate">{{ u.email }}</p>
                    <span class="inline-block mt-1 text-xs px-2 py-0.5 rounded-full font-medium" :class="rolePillClass(u.role)">
                    {{ roleLabel(u.role) }}
                    </span>
                </div>
                </div>
                <div class="flex items-center gap-4 shrink-0 self-end sm:self-center">
                <button class="font-medium text-purple-600 hover:text-purple-700" @click="openEdit(u)">Permisos</button>
                <button class="font-medium text-rose-600 hover:text-rose-700" @click="openDelete(u)">Eliminar</button>
                </div>
            </div>
        </div>
    </div>
     <div v-else class="text-center py-10 px-4 bg-white rounded-lg shadow">
        <p class="text-slate-500">No se encontraron usuarios que coincidan con los filtros.</p>
    </div>


    <div v-if="showAdd" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showAdd = false"></div>
      <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl p-6">
        <h2 class="text-xl font-semibold mb-4">Invitar Nuevo Usuario</h2>
        <form @submit.prevent="submitNew" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1" for="add-name">Nombre completo</label>
            <input v-model.trim="formAdd.name" id="add-name" type="text"
              class="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-teal-400" placeholder="Ej: Juan Pérez" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1" for="add-email">Correo Electrónico</label>
            <input v-model.trim="formAdd.email" id="add-email" type="email"
              class="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-teal-400" placeholder="nombre@empresa.com" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1" for="add-role">Rol del usuario</label>
            <select v-model="formAdd.role" id="add-role" class="w-full h-11 border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-400">
              <option disabled value="">Selecciona un rol…</option>
              <option value="admin">Administrador</option>
              <option value="manager">Manager</option>
              <option value="worker">Worker</option>
              <option value="viewer">Viewer</option>
            </select>
          </div>
          <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>
          <div class="space-y-2 pt-2">
            <button type="submit" class="w-full h-11 rounded-lg bg-teal-500 text-white font-semibold hover:bg-teal-600">Enviar Invitación</button>
            <button type="button" @click="showAdd = false" class="w-full h-11 rounded-lg border hover:bg-slate-50">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showEdit" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showEdit = false"></div>
      <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl p-6">
        <h2 class="text-xl font-semibold mb-2">Cambiar Rol</h2>
        <p class="text-slate-600 mb-4">Estás editando los permisos para <strong class="font-medium">{{ formEdit.name }}</strong>.</p>
        <form @submit.prevent="submitEdit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1" for="edit-role">Nuevo rol para el usuario</label>
            <select v-model="formEdit.role" id="edit-role" class="w-full h-11 border rounded-lg px-3 py-2 focus:ring-2 focus:ring-purple-400">
              <option value="admin">Administrador</option>
              <option value="manager">Manager</option>
              <option value="worker">Worker</option>
              <option value="viewer">Viewer</option>
            </select>
          </div>
          <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>
          <div class="space-y-2 pt-2">
            <button type="submit" class="w-full h-11 rounded-lg bg-purple-600 text-white font-semibold hover:bg-purple-700">Actualizar Rol</button>
            <button type="button" @click="showEdit = false" class="w-full h-11 rounded-lg border hover:bg-slate-50">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showDelete" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showDelete = false"></div>
      <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl p-6 text-center">
        <h2 class="text-xl font-semibold mb-2 text-rose-600">¿Estás seguro?</h2>
        <p class="text-slate-600 mb-4">
          Vas a eliminar a <strong class="font-medium">{{ currentUser?.name }}</strong> de la empresa.
          Esta acción no se puede deshacer.
        </p>
        <p v-if="error" class="text-red-600 text-sm mb-4">{{ error }}</p>
        <div class="flex gap-3 justify-center">
            <button @click="showDelete = false" class="w-full h-11 rounded-lg border font-semibold hover:bg-slate-50">No, cancelar</button>
            <button @click="submitDelete" class="w-full h-11 rounded-lg bg-rose-600 text-white font-semibold hover:bg-rose-700">Sí, eliminar</button>
        </div>
      </div>
    </div>

  </section>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
// Importamos el servicio de API de forma directa y simplificada
import userService from '@/services/usersApi.service.js';

/* --- Estado del Componente --- */
const users = ref([]);
const currentUser = ref(null);
const error = ref('');

// Estados de los modales
const showAdd = ref(false);
const showEdit = ref(false);
const showDelete = ref(false);

// Formularios reactivos
const formAdd = reactive({ name: '', email: '', role: '' });
const formEdit = reactive({ id: null, name: '', role: '' });

// Filtros
const search = ref('');
const roleFilter = ref('');

/* --- Ciclo de Vida --- */
onMounted(() => {
  fetchUsers();
});

/* --- Métodos de Datos --- */
async function fetchUsers() {
  try {
    const response = await userService.list();
    // 👇 CAMBIO: Leemos la estructura plana que ahora nos da la API
    users.value = response.data.map(u => ({
      id: u.id,
      userId: u.id, // El ID que devuelve la API es el del usuario
      name: u.name,
      email: u.email,
      role: u.rol,
      color: randomColor()
    }));
  } catch (e) {
    console.error("Error al cargar usuarios:", e);
    error.value = "No se pudieron cargar los usuarios.";
  }
}

/* --- Propiedades Computadas --- */
const filteredUsers = computed(() => {
  const q = search.value.toLowerCase().trim();
  if (!users.value) return [];
  return users.value.filter(u => {
    const matchText = !q || u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q);
    const matchRole = !roleFilter.value || u.role === roleFilter.value;
    return matchText && matchRole;
  });
});

const listForDesktop = computed(() => filteredUsers.value);

/* --- Métodos de Modales y Formularios --- */

// AÑADIR USUARIO
function openAddUser() {
  error.value = '';
  Object.assign(formAdd, { name: '', email: '', role: '' });
  showAdd.value = true;
}

async function submitNew() {
  error.value = '';
  if (!formAdd.name || !formAdd.email || !formAdd.role) {
    error.value = 'Todos los campos son obligatorios.';
    return;
  }
  try {
    const payload = {
      nombre_completo: formAdd.name,
      email: formAdd.email,
      rol: formAdd.role
    };
    // Esta llamada es EXITOSA
    const response = await userService.create(payload);
    const createdUser = response.data;

    // Esta es la parte que corregimos para que lea bien la respuesta
    users.value.unshift({
        id: createdUser.id,
        userId: createdUser.id,
        name: createdUser.name,
        email: formAdd.email,
        role: createdUser.rol,
        color: randomColor()
    });
    
    showAdd.value = false; // El modal se cierra correctamente
  } catch (e) {
    // Este bloque se está ejecutando por error, pero ya no lo hará con el cambio
    const errorMsg = e.response?.data?.detail || 'Error al guardar el usuario.';
    error.value = errorMsg;
    console.error("Error residual:", e);
  }
}

// EDITAR PERMISOS
function openEdit(user) {
  currentUser.value = user;
  formEdit.id = user.id;
  formEdit.name = user.name;
  formEdit.role = user.role;
  error.value = '';
  showEdit.value = true;
}

async function submitEdit() {
  if (!formEdit.role) {
    error.value = 'Debes seleccionar un rol.';
    return;
  }
  try {
    const response = await userService.update(formEdit.id, { rol: formEdit.role });
    const updatedUser = response.data;
    const index = users.value.findIndex(u => u.id === formEdit.id);
    if (index !== -1) {
      users.value[index].role = updatedUser.rol;
    }
    showEdit.value = false;
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al actualizar el rol.';
  }
}

// ELIMINAR USUARIO
function openDelete(user) {
  currentUser.value = user;
  error.value = '';
  showDelete.value = true;
}

async function submitDelete() {
  try {
    await userService.remove(currentUser.value.id);
    users.value = users.value.filter(u => u.id !== currentUser.value.id);
    showDelete.value = false;
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al eliminar el usuario.';
  }
}

function clearFilters() {
  search.value = '';
  roleFilter.value = '';
}

/* --- Funciones de Utilidad --- */
function initials(name) {
  if (!name) return '';
  return name.split(' ').map(p => p[0]).slice(0, 2).join('').toUpperCase();
}
function roleLabel(v) {
  const labels = { admin: 'Administrador', manager: 'Manager', worker: 'Worker', viewer: 'Viewer' };
  return labels[v] || v;
}
function rolePillClass(v) {
  const classes = {
    admin: 'bg-purple-100 text-purple-700',
    manager: 'bg-orange-100 text-orange-700',
    worker: 'bg-blue-100 text-blue-700',
    viewer: 'bg-slate-100 text-slate-600'
  };
  return classes[v];
}
function randomColor() {
  const p = ['#8b5cf6', '#f97316', '#3b82f6', '#ef4444', '#14b8a6'];
  return p[Math.floor(Math.random() * p.length)];
}

function pillColor(v, solid = false) {
  const map = {
    admin: ['#ede9fe', '#8b5cf6'],
    manager: ['#ffedd5', '#f97316'],
    worker: ['#dbeafe', '#3b82f6'],
    viewer: ['#f1f5f9', '#475569']
  };
  const pair = map[v] || ['#e5e7eb', '#6b7280'];
  return solid ? pair[1] : pair[0];
}
</script>

<style scoped>
.usuarios {
  padding: 1.25rem;
}
@media (min-width: 1024px) {
  .usuarios {
    padding: 2rem;
  }
}
</style>