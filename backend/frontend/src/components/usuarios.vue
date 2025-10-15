<template>
  <section class="usuarios max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between mb-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-slate-800">Gestión de Usuarios</h1>
        <p class="text-slate-500">Administra los usuarios, sus roles y permisos dentro del sistema.</p>
      </div>
      <button
        class="w-full sm:w-auto px-4 py-2 rounded-md bg-teal-500 text-white hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
        @click="openAddUser"
      >+ Agregar Nuevo Usuario</button>
    </div>

    <div class="bg-white rounded-lg shadow p-4 mb-4">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div class="relative">
          <input v-model.trim="search" type="text" placeholder="Buscar por nombre o correo…"
            class="w-full pl-10 pr-3 py-2 border rounded-lg focus:ring-2 focus:ring-teal-400 focus:border-teal-400" />
          <svg class="pointer-events-none absolute left-3 top-2.5 h-5 w-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
        <div>
          <select v-model="roleFilter"
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-teal-400 focus:border-teal-400">
            <option value="">Todos los roles</option>
            <option value="admin">Administrador</option>
            <option value="manager">Manager</option>
            <option value="worker">Worker</option>
            <option value="viewer">Viewer</option>
          </select>
        </div>
        <div class="flex gap-2">
          <button class="w-full sm:w-auto px-3 py-2 rounded border hover:bg-slate-50" @click="clearFilters">Limpiar</button>
          <div class="hidden sm:flex items-center text-sm text-slate-500">
            {{ filteredUsers.length }} resultado(s)
          </div>
        </div>
      </div>
      <div class="sm:hidden text-xs text-slate-500 mt-2">
        {{ filteredUsers.length }} resultado(s)
      </div>
    </div>

    <div v-for="u in listForDesktop" :key="u.id || u.email" class="bg-white rounded-lg shadow p-4 sm:p-5 mb-3">
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div class="flex items-center gap-4 flex-1 min-w-0">
          <div class="h-10 w-10 rounded-full flex items-center justify-center text-white font-semibold shrink-0"
               :style="{ backgroundColor: u.color || pillColor(u.role, true) }">
            {{ initials(u.name) }}
          </div>
          <div class="min-w-0">
            <p class="font-semibold text-slate-800 truncate">{{ u.name }}</p>
            <p class="text-slate-500 text-sm truncate">{{ u.email }}</p>
            <span class="inline-block mt-1 text-xs px-2 py-0.5 rounded-full" :class="rolePillClass(u.role)">
              {{ roleLabel(u.role) }}
            </span>
          </div>
        </div>
        <div class="flex items-center gap-4 shrink-0 self-end sm:self-center">
          <button class="font-medium text-teal-600 hover:text-teal-700" @click="openEditUser(u)">Editar</button>
          <button class="font-medium text-purple-600 hover:text-purple-700" @click="openEdit(u)">Permisos</button>
          <button class="font-medium text-rose-600 hover:text-rose-700" @click="openDelete(u)">Eliminar</button>
        </div>
      </div>
    </div>

    <div class="sm:hidden flex items-center justify-between mt-4" v-if="totalPagesMobile > 1">
      </div>

    <div v-if="showAdd" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeAdd"></div>
      <div class="relative w-full max-w-md sm:max-w-lg bg-white rounded-2xl shadow-2xl p-5 sm:p-6">
        <h2 class="text-xl font-semibold mb-4">Nuevo Usuario</h2>
        <form @submit.prevent="submitNew" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Nombre completo</label>
            <input v-model.trim="form.name" type="text"
              class="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-teal-400" placeholder="Ej: Juan Pérez" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Correo</label>
            <input v-model.trim="form.email" type="email"
              class="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-teal-400" placeholder="nombre@empresa.com" />
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">Rol del usuario</label>
            <select v-model="form.role" class="w-full h-11 border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-400">
              <option disabled value="">Selecciona un rol…</option>
              <option value="admin">Administrador</option>
              <option value="manager">Manager</option>
              <option value="worker">Worker</option>
              <option value="viewer">Viewer</option>
            </select>
          </div>

          <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>
          <div class="space-y-2 pt-2">
            <button type="submit" class="w-full h-11 rounded-lg bg-teal-500 text-white hover:bg-teal-600">Guardar</button>
            <button type="button" @click="closeAdd" class="w-full h-11 rounded-lg border">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showEdit" class="fixed inset-0 z-50"></div>
    <div v-if="showEditUser" class="fixed inset-0 z-50"></div>
    <div v-if="showDelete" class="fixed inset-0 z-50"></div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
// 👇 1. Se corrige la importación para usar el servicio principal
import { getUsersService } from '@/services/users.service.js';

let userService; // Variable para mantener la instancia del servicio

/* --- Estado del Componente --- */
const users = ref([]);
const showAdd = ref(false);
const showEdit = ref(false);
const showEditUser = ref(false);
const showDelete = ref(false);

const error = ref('');
const form = reactive({
  name: '',
  email: '',
  role: ''
});

const search = ref('');
const roleFilter = ref('');
// 👇 2. Se elimina la variable 'pageMobile' que no se usa
// const pageMobile = ref(1);

/* --- Ciclo de Vida --- */
onMounted(async () => {
  try {
    userService = await getUsersService();
    const userList = await userService.list();
    users.value = userList.map(u => ({ ...u, color: randomColor() }));
  } catch (e) {
    console.error("Error al cargar la lista de usuarios:", e);
  }
});

/* --- Propiedades Computadas --- */
const filteredUsers = computed(() => {
  const q = search.value.toLowerCase().trim();
  if (!users.value) return [];
  return users.value.filter(u => {
    const matchText = !q || (u.name && u.name.toLowerCase().includes(q)) || (u.email && u.email.toLowerCase().includes(q));
    const matchRole = !roleFilter.value || u.role === roleFilter.value;
    return matchText && matchRole;
  });
});

const listForDesktop = computed(() => filteredUsers.value);
const totalPagesMobile = computed(() => 1); // Simplificado

/* --- Métodos --- */
function openAddUser() {
  error.value = '';
  form.name = '';
  form.email = '';
  form.role = '';
  showAdd.value = true;
}

function closeAdd() {
  showAdd.value = false;
}

async function submitNew() {
  error.value = '';
  if (!form.name || !form.email || !form.role) {
    error.value = 'Todos los campos son obligatorios.';
    return;
  }
  try {
    const newUser = {
      name: form.name,
      email: form.email,
      role: form.role
    };
    const createdUser = await userService.create(newUser);
    users.value.unshift({ ...createdUser, color: randomColor() });
    closeAdd();
  } catch (e) {
    error.value = e.response?.data?.error || 'Error al guardar el usuario.';
  }
}

// TODO: Implementar lógica de editar y eliminar
function openEditUser(u) { console.log('Editar usuario:', u); showEditUser.value = true; }
function openEdit(u) { console.log('Editar permisos:', u); showEdit.value = true; }
function openDelete(u) { console.log('Eliminar:', u); showDelete.value = true; }
function clearFilters() { search.value = ''; roleFilter.value = ''; }

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
function randomColor() {
  const p = ['#8b5cf6', '#f97316', '#3b82f6', '#ef4444', '#14b8a6'];
  return p[Math.floor(Math.random() * p.length)];
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