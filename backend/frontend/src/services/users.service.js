// src/services/users.service.js
import { mockUsersService } from './usersMock.service.js'
import { apiUsersService } from './usersApi.service.js'

// Usa el mock mientras no tengas backend
const USE_MOCK = true;

export function getUsersService() {
  return USE_MOCK ? mockUsersService() : apiUsersService();
}
