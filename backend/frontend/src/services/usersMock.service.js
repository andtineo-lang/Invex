const KEY = 'invex.users';

function read() {
  const raw = localStorage.getItem(KEY);
  return raw ? JSON.parse(raw) : [
    { id:'u1', name:'Juan Pérez',     email:'juan.perez@empresa.com',    role:'admin'   },
    { id:'u2', name:'María Silva',    email:'maria.silva@empresa.com',   role:'worker'  },
    { id:'u3', name:'Roberto García', email:'roberto.garcia@empresa.com',role:'manager' },
  ];
}
function write(users){ localStorage.setItem(KEY, JSON.stringify(users)); }
function uid(){ return (crypto.randomUUID?.() || 'u_' + Math.random().toString(36).slice(2,9)); }

export function mockUsersService(){
  if (!localStorage.getItem(KEY)) write(read());
  return {
    async list(){ return read(); },

    async create(u){
      const users = read();
      const exists = users.some(x => x.email.toLowerCase() === u.email.toLowerCase());
      if (exists) throw new Error('EMAIL_EXISTS');
      const nu = { id: uid(), ...u };
      users.unshift(nu); write(users);
      return nu;
    },

    async emailExists(email, exceptId=null){
      return read().some(x =>
        x.email.toLowerCase() === email.toLowerCase() &&
        (exceptId ? x.id !== exceptId : true)
      );
    },

    // actualizar campos (name/email/role...)
    async update(id, patch){
      const users = read();
      const idx = users.findIndex(u => u.id === id);
      if (idx === -1) throw new Error('NOT_FOUND');

      if (patch.email && await this.emailExists(patch.email, id)) {
        throw new Error('EMAIL_EXISTS');
      }
      users[idx] = { ...users[idx], ...patch };
      write(users);
      return users[idx];
    },

    async remove(id){
      const users = read();
      const idx = users.findIndex(u => u.id === id);
      if (idx === -1) throw new Error('NOT_FOUND');
      const [deleted] = users.splice(idx, 1);
      write(users);
      return deleted;
    }
  };
}
