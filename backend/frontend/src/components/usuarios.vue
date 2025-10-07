<template>
  <section class="usuarios max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between mb-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold">Gestión de Usuarios</h1>
        <p class="text-slate-500">Administra los usuarios, sus roles y permisos dentro del sistema.</p>
      </div>
      <button
        class="w-full sm:w-auto px-4 py-2 rounded-md bg-emerald-600 text-white hover:bg-emerald-700"
        @click="openAddUser"
      >+ Agregar Nuevo Usuario</button>
    </div>

    <!-- Filtros -->
    <div class="bg-white rounded-lg shadow p-4 mb-4">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div class="relative">
          <input v-model.trim="search" type="text" placeholder="Buscar por nombre o correo…"
            class="w-full pl-10 pr-3 py-2 border rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500" />
          <svg class="pointer-events-none absolute left-3 top-2.5 h-5 w-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
        <div>
          <select v-model="roleFilter"
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">
            <option value="">Todos los roles</option>
            <option value="admin">Administrador</option>
            <option value="manager">Manager</option>
            <option value="worker">Worker</option>
            <option value="viewer">Viewer</option>
          </select>
        </div>
        <div class="flex gap-2">
          <button class="w-full sm:w-auto px-3 py-2 rounded border" @click="clearFilters">Limpiar</button>
          <div class="hidden sm:flex items-center text-sm text-slate-500">
            {{ filteredUsers.length }} resultado(s)
          </div>
        </div>
      </div>
      <div class="sm:hidden text-xs text-slate-500 mt-2">
        {{ filteredUsers.length }} resultado(s)
      </div>
    </div>

    <!-- Lista -->
    <div v-for="u in listForDesktop" :key="u.id || u.email" class="bg-white rounded-lg shadow p-4 sm:p-5 mb-3">
      <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div class="flex items-center gap-4">
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

        <!-- Acciones -->
        <div class="grid grid-cols-2 sm:flex sm:flex-row gap-2">
          <button class="px-3 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                  @click="openEditUser(u)">Editar</button>
          <button class="px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                  @click="openEdit(u)">Permisos</button>
          <button class="col-span-2 sm:col-span-1 px-3 py-2 bg-rose-600 text-white rounded hover:bg-rose-700"
                  @click="openDelete(u)">Eliminar</button>
        </div>
      </div>
    </div>

    <!-- Paginación móvil -->
    <div class="sm:hidden flex items-center justify-between mt-4" v-if="totalPagesMobile > 1">
      <button class="px-3 py-2 rounded border disabled:opacity-40"
              :disabled="pageMobile === 1" @click="pageMobile--">Anterior</button>
      <div class="text-sm">Página {{ pageMobile }} de {{ totalPagesMobile }}</div>
      <button class="px-3 py-2 rounded border disabled:opacity-40"
              :disabled="pageMobile === totalPagesMobile" @click="pageMobile++">Siguiente</button>
    </div>

    <!-- Modal Crear -->
    <div v-if="showAdd" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeAdd"></div>
      <div class="relative w-full max-w-md sm:max-w-lg bg-white rounded-2xl shadow-2xl p-5 sm:p-6">
        <h2 class="text-xl font-semibold mb-4">Nuevo Usuario</h2>
        <form @submit.prevent="submitNew" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Nombre completo</label>
            <input v-model.trim="form.name" type="text"
              class="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              placeholder="Ej: Juan Pérez" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Correo</label>
            <input v-model.trim="form.email" type="email"
              class="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              placeholder="nombre@empresa.com" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Rol del usuario</label>
            <select v-model="form.role"
              class="w-full h-11 border rounded-lg px-3 py-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">
              <option disabled value="">Selecciona un rol…</option>
              <option value="admin">Administrador</option>
              <option value="manager">Manager</option>
              <option value="worker">Worker</option>
              <option value="viewer">Viewer</option>
            </select>
            <!-- Descripción del rol (crear) -->
            <p class="text-xs text-slate-500 mt-1" v-if="form.role">{{ roleHelpText(form.role) }}</p>
          </div>

          <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>

          <div class="space-y-2 pt-2">
            <button type="button" @click="closeAdd"
              class="w-full h-11 rounded-lg border border-slate-300 bg-white text-slate-800 hover:bg-slate-50">
              Cancelar
            </button>
            <button type="submit"
              class="w-full h-11 rounded-lg bg-emerald-600 text-white hover:bg-emerald-700">
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Editar Permisos (con descripción del rol) -->
    <div v-if="showEdit" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeEdit"></div>
      <div class="relative w-full max-w-md sm:max-w-lg bg-white rounded-2xl shadow-2xl p-5 sm:p-6">
        <h2 class="text-xl font-semibold mb-1">Editar permisos</h2>
        <p class="text-slate-500 mb-4 truncate">{{ editTarget?.name }} — {{ editTarget?.email }}</p>

        <form @submit.prevent="submitEdit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Rol del usuario</label>
            <select v-model="editForm.role"
              class="w-full h-11 border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="admin">Administrador</option>
              <option value="manager">Manager</option>
              <option value="worker">Worker</option>
              <option value="viewer">Viewer</option>
            </select>
            <!-- Descripción del rol (editar permisos) -->
            <p class="text-xs text-slate-500 mt-1" v-if="editForm.role">{{ roleHelpText(editForm.role) }}</p>
          </div>

          <p v-if="editError" class="text-red-600 text-sm">{{ editError }}</p>

          <div class="space-y-2 pt-2">
            <button type="button" @click="closeEdit"
              class="w-full h-11 rounded-lg border border-slate-300 bg-white text-slate-800 hover:bg-slate-50">
              Cancelar
            </button>
            <button type="submit"
              class="w-full h-11 rounded-lg bg-blue-600 text-white hover:bg-blue-700">
              Guardar cambios
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Editar Usuario -->
    <div v-if="showEditUser" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeEditUser"></div>
      <div class="relative w-full max-w-md sm:max-w-lg bg-white rounded-2xl shadow-2xl p-5 sm:p-6">
        <h2 class="text-xl font-semibold mb-4">Editar usuario</h2>
        <form @submit.prevent="submitEditUser" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Nombre</label>
            <input v-model.trim="editUserForm.name" type="text"
              class="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Correo</label>
            <input v-model.trim="editUserForm.email" type="email"
              class="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Rol</label>
            <select v-model="editUserForm.role"
              class="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
              <option value="admin">Administrador</option>
              <option value="manager">Manager</option>
              <option value="worker">Worker</option>
              <option value="viewer">Viewer</option>
            </select>
             <p class="text-xs text-slate-500 mt-1" v-if="editUserForm.role">
    {{ roleHelpText(editUserForm.role) }}
  </p>
          </div>

          <p v-if="editUserError" class="text-red-600 text-sm">{{ editUserError }}</p>

          <div class="space-y-2 pt-2">
            <button type="button" @click="closeEditUser"
              class="w-full h-11 rounded-lg border border-slate-300 bg-white text-slate-800 hover:bg-slate-50">Cancelar</button>
            <button type="submit"
              class="w-full h-11 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700">Guardar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Eliminar -->
    <div v-if="showDelete" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeDelete"></div>
      <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl p-5 sm:p-6">
        <h2 class="text-lg font-semibold">Eliminar usuario</h2>
        <p class="text-slate-600 mt-2">¿Seguro que deseas eliminar a <strong>{{ deleteTarget?.name }}</strong>? Esta acción no se puede deshacer.</p>
        <div class="space-y-2 mt-5">
          <button class="w-full h-11 rounded-lg border" @click="closeDelete">Cancelar</button>
          <button class="w-full h-11 rounded-lg bg-rose-600 text-white hover:bg-rose-700" @click="confirmDelete">Eliminar</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { getUsersService } from '@/services/users.service.js'

/* Estado base */
const users = ref([])
const showAdd = ref(false)
const showEdit = ref(false)
const showEditUser = ref(false)
const showDelete = ref(false)

const error = ref('')
const editError = ref('')
const editUserError = ref('')

const form = reactive({ name: '', email: '', role: '' })
const editForm = reactive({ id: '', role: '' })
const editUserForm = reactive({ id:'', name:'', email:'', role:'' })

const editTarget = ref(null)
const deleteTarget = ref(null)

let svc

/* Filtros y paginación móvil */
const search = ref('')
const roleFilter = ref('')
const pageMobile = ref(1)
const pageSizeMobile = 6

onMounted(async () => {
  svc = await getUsersService()
  const list = await svc.list()
  users.value = list.map(u => ({ ...u, color: u.color || randomColor() }))
})

/* Filtros */
const filteredUsers = computed(() => {
  const q = search.value.toLowerCase().trim()
  return users.value.filter(u => {
    const matchText = !q || u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q)
    const matchRole = !roleFilter.value || u.role === roleFilter.value
    return matchText && matchRole
  })
})
const listForDesktop = computed(() => filteredUsers.value)
const totalPagesMobile = computed(() => Math.max(1, Math.ceil(filteredUsers.value.length / pageSizeMobile)))
watch([filteredUsers, totalPagesMobile], () => {
  if (pageMobile.value > totalPagesMobile.value) pageMobile.value = 1
})

/* Alta */
function openAddUser(){ error.value=''; form.name=''; form.email=''; form.role=''; showAdd.value=true }
function closeAdd(){ showAdd.value=false }
function isEmail(v){ return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) }

async function submitNew(){
  error.value=''
  if(!form.name){ error.value='El nombre es obligatorio.'; return }
  if(!isEmail(form.email)){ error.value='Correo inválido.'; return }
  if(!form.role){ error.value='Selecciona un rol.'; return }
  if(await svc.emailExists(form.email)){ error.value='Ese correo ya existe.'; return }
  try{
    const created = await svc.create({ name: form.name, email: form.email, role: form.role })
    users.value = [{ ...created, color: randomColor() }, ...users.value]
    closeAdd()
  }catch(e){
    error.value = (e && e.message === 'EMAIL_EXISTS') ? 'Ese correo ya existe.' : 'Error al guardar.'
  }
}

/* Editar permisos (rol) */
function openEdit(u){ editError.value=''; editTarget.value = u; editForm.id = u.id; editForm.role = u.role; showEdit.value = true }
function closeEdit(){ showEdit.value = false }
function roleHelpText(role){
  switch(role){
    case 'admin': return 'Acceso total al sistema, gestión de usuarios y configuración.'
    case 'manager': return 'Gestiona inventario, reportes y aprobaciones.'
    case 'worker': return 'Opera inventario y tareas diarias.'
    default: return 'Solo lectura.'
  }
}
async function submitEdit(){
  editError.value=''
  if(!editForm.role){ editError.value='Selecciona un rol.'; return }
  try{
    const updated = await svc.update(editForm.id, { role: editForm.role })
    users.value = users.value.map(u => u.id === updated.id ? { ...u, role: updated.role } : u)
    closeEdit()
  }catch(e){ editError.value = 'No se pudo actualizar.' }
}

/* Editar usuario (nombre/correo/rol) */
function openEditUser(u){
  editUserError.value=''
  editUserForm.id = u.id
  editUserForm.name = u.name
  editUserForm.email = u.email
  editUserForm.role = u.role
  showEditUser.value = true
}
function closeEditUser(){ showEditUser.value = false }

async function submitEditUser(){
  editUserError.value=''
  if(!editUserForm.name){ editUserError.value='El nombre es obligatorio.'; return }
  if(!isEmail(editUserForm.email)){ editUserError.value='Correo inválido.'; return }

  if(await svc.emailExists(editUserForm.email, editUserForm.id)){
    editUserError.value = 'Ese correo ya existe.'; return
  }

  try{
    const updated = await svc.update(editUserForm.id, {
      name: editUserForm.name,
      email: editUserForm.email,
      role: editUserForm.role
    })
    users.value = users.value.map(u => u.id === updated.id ? { ...u, ...updated } : u)
    closeEditUser()
  }catch(e){
    editUserError.value = (e && e.message === 'EMAIL_EXISTS') ? 'Ese correo ya existe.' : 'No se pudo actualizar.'
  }
}

/* Eliminar */
function openDelete(u){ deleteTarget.value = u; showDelete.value = true }
function closeDelete(){ showDelete.value = false }
async function confirmDelete(){
  try{
    await svc.remove(deleteTarget.value.id)
    users.value = users.value.filter(u => u.id !== deleteTarget.value.id)
    closeDelete()
  }catch{ closeDelete() }
}

/* Utilidades */
function clearFilters(){ search.value=''; roleFilter.value=''; pageMobile.value=1 }
function initials(name){ return name.split(' ').map(p=>p[0]).slice(0,2).join('').toUpperCase() }
function roleLabel(v){ return ({admin:'Administrador', manager:'Manager', worker:'Worker', viewer:'Viewer'})[v] || v }
function rolePillClass(v){
  return {admin:'bg-blue-100 text-blue-700', manager:'bg-emerald-100 text-emerald-700',
          worker:'bg-purple-100 text-purple-700', viewer:'bg-slate-100 text-slate-700'}[v]
}
function pillColor(v, solid=false){
  const map = { admin:['#dbeafe','#3b82f6'], manager:['#d1fae5','#10b981'],
                worker:['#f3e8ff','#8b5cf6'], viewer:['#f1f5f9','#0f172a'] }
  const pair = map[v] || ['#e5e7eb','#6b7280']; return solid ? pair[1] : pair[0]
}
function randomColor(){ const p=['#3b82f6','#22c55e','#a855f7','#f59e0b','#ef4444','#14b8a6']; return p[Math.floor(Math.random()*p.length)] }
</script>

<style scoped>
.usuarios { padding: 1.25rem; }
@media (min-width: 1024px) { .usuarios { padding: 2rem; } }
</style>
