// Si luego usas axios: import axios from 'axios'; const client = axios.create({ baseURL:'/api' });

export function apiUsersService(){
  console.warn('[usersApi.service] Placeholder. Usa USE_MOCK=true hasta tener backend.');
  return {
    async list(){ return []; },
    async create(u){ return { id:'api_tmp', ...u }; },
    async emailExists(){ return false; },
    async update(id, patch){ return { id, ...patch }; } // ajusta cuando tengas API real
  };
}
