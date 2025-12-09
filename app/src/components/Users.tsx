import React, { useState, useEffect, useCallback } from 'react';
import { Header } from './Header';
import { Footer } from './Footer';
import { useAuth } from '../hooks/useAuth';

interface User {
  username: string;
  email: string;
  name?: string;
  tana_api_key?: string;
  node_id?: string;
  created_at?: string;
  last_login?: string;
  is_active?: boolean;
}

interface CreateUserData {
  username: string;
  password: string;
  email: string;
  name?: string;
  tana_api_key?: string;
  node_id?: string;
}

export function Users() {
  const { token } = useAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [selectedUsers, setSelectedUsers] = useState<Set<string>>(new Set());
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Form states
  const [createUserForm, setCreateUserForm] = useState<CreateUserData>({
    username: '',
    password: '',
    email: '',
    name: '',
    tana_api_key: '',
    node_id: '',
  });

  const [passwordForm, setPasswordForm] = useState({
    username: '',
    password: '',
  });

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const fetchUsers = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/users`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }

      const data = await response.json();
      setUsers(data.users || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching users');
    } finally {
      setLoading(false);
    }
  }, [token, API_BASE_URL]);

  useEffect(() => {
    if (token) {
      fetchUsers();
    }
  }, [token, fetchUsers]);

  const toggleUserSelection = (username: string) => {
    const newSelection = new Set(selectedUsers);
    if (newSelection.has(username)) {
      newSelection.delete(username);
    } else {
      newSelection.add(username);
    }
    setSelectedUsers(newSelection);
  };

  const handleDeleteSelected = async () => {
    if (selectedUsers.size === 0) return;

    if (!confirm(`Are you sure you want to delete ${selectedUsers.size} user(s)?`)) {
      return;
    }

    setActionLoading(true);
    setMessage('');

    try {
      const deletePromises = Array.from(selectedUsers).map((username) =>
        fetch(`${API_BASE_URL}/api/users/${username}`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
      );

      await Promise.all(deletePromises);

      setMessage(`Successfully deleted ${selectedUsers.size} user(s)`);
      setSelectedUsers(new Set());
      fetchUsers();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error deleting users');
    } finally {
      setActionLoading(false);
    }
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setActionLoading(true);
    setMessage('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/users`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(createUserForm),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create user');
      }

      setMessage('User created successfully');
      setShowCreateModal(false);
      setCreateUserForm({
        username: '',
        password: '',
        email: '',
        name: '',
        tana_api_key: '',
        node_id: '',
      });
      fetchUsers();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error creating user');
    } finally {
      setActionLoading(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setActionLoading(true);
    setMessage('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/users/${passwordForm.username}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ password: passwordForm.password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update password');
      }

      setMessage('Password updated successfully');
      setShowPasswordModal(false);
      setPasswordForm({ username: '', password: '' });
      fetchUsers();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error updating password');
    } finally {
      setActionLoading(false);
    }
  };

  const openPasswordModal = (username: string) => {
    setPasswordForm({ username, password: '' });
    setShowPasswordModal(true);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-tana-bg text-tana-text flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p>Loading users...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-tana-bg text-tana-text">
      <Header title="User Management" />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-300">
            {error}
          </div>
        )}

        {message && (
          <div className="mb-6 p-4 bg-green-500/20 border border-green-500/50 rounded-lg text-green-300">
            {message}
          </div>
        )}

        <div className="bg-tana-card border border-tana-border rounded-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-white">Users</h2>
            <div className="flex space-x-4">
              {selectedUsers.size > 0 && (
                <button
                  onClick={handleDeleteSelected}
                  disabled={actionLoading}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Delete Selected ({selectedUsers.size})
                </button>
              )}
              <button
                onClick={() => setShowCreateModal(true)}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Add User
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-tana-border">
                  <th className="text-left p-4">
                    <input
                      type="checkbox"
                      checked={selectedUsers.size === users.length && users.length > 0}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedUsers(new Set(users.map((u) => u.username)));
                        } else {
                          setSelectedUsers(new Set());
                        }
                      }}
                      className="rounded border-gray-300 bg-tana-bg text-indigo-600 focus:ring-indigo-500"
                    />
                  </th>
                  <th className="text-left p-4 font-medium text-white">Username</th>
                  <th className="text-left p-4 font-medium text-white">Email</th>
                  <th className="text-left p-4 font-medium text-white">Tana API Key</th>
                  <th className="text-left p-4 font-medium text-white">Node ID</th>
                  <th className="text-left p-4 font-medium text-white">Status</th>
                  <th className="text-left p-4 font-medium text-white">Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="text-center p-8 text-tana-muted">
                      No users found
                    </td>
                  </tr>
                ) : (
                  users.map((user) => (
                    <tr
                      key={user.username}
                      className="border-b border-tana-border hover:bg-white/5"
                    >
                      <td className="p-4">
                        <input
                          type="checkbox"
                          checked={selectedUsers.has(user.username)}
                          onChange={() => toggleUserSelection(user.username)}
                          className="rounded border-gray-300 bg-tana-bg text-indigo-600 focus:ring-indigo-500"
                        />
                      </td>
                      <td className="p-4 font-medium text-white">{user.username}</td>
                      <td className="p-4 text-tana-text">{user.email}</td>
                      <td className="p-4">
                        <span className="text-xs text-tana-muted font-mono bg-black/30 px-2 py-1 rounded">
                          {user.tana_api_key
                            ? `${user.tana_api_key.substring(0, 8)}...`
                            : 'Not set'}
                        </span>
                      </td>
                      <td className="p-4">
                        <span className="text-xs text-tana-muted font-mono bg-black/30 px-2 py-1 rounded">
                          {user.node_id || 'Not set'}
                        </span>
                      </td>
                      <td className="p-4">
                        <span
                          className={`text-xs px-2 py-1 rounded ${
                            user.is_active === false
                              ? 'bg-red-500/20 text-red-300'
                              : 'bg-green-500/20 text-green-300'
                          }`}
                        >
                          {user.is_active === false ? 'Inactive' : 'Active'}
                        </span>
                      </td>
                      <td className="p-4">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => openPasswordModal(user.username)}
                            className="text-indigo-400 hover:text-indigo-300 text-sm"
                          >
                            Change Password
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      <Footer />

      {/* Create User Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-tana-card border border-tana-border rounded-xl p-6 max-w-md w-full mx-4">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold text-white">Create New User</h3>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-tana-muted hover:text-white transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            <form onSubmit={handleCreateUser} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-white mb-1">Username</label>
                <input
                  type="text"
                  required
                  value={createUserForm.username}
                  onChange={(e) =>
                    setCreateUserForm({ ...createUserForm, username: e.target.value })
                  }
                  className="w-full px-3 py-2 bg-tana-bg border border-tana-border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-1">Email</label>
                <input
                  type="email"
                  required
                  value={createUserForm.email}
                  onChange={(e) => setCreateUserForm({ ...createUserForm, email: e.target.value })}
                  className="w-full px-3 py-2 bg-tana-bg border border-tana-border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-1">Password</label>
                <input
                  type="password"
                  required
                  value={createUserForm.password}
                  onChange={(e) =>
                    setCreateUserForm({ ...createUserForm, password: e.target.value })
                  }
                  className="w-full px-3 py-2 bg-tana-bg border border-tana-border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-1">Name (optional)</label>
                <input
                  type="text"
                  value={createUserForm.name}
                  onChange={(e) => setCreateUserForm({ ...createUserForm, name: e.target.value })}
                  className="w-full px-3 py-2 bg-tana-bg border border-tana-border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-1">
                  Tana API Key (optional)
                </label>
                <input
                  type="text"
                  value={createUserForm.tana_api_key}
                  onChange={(e) =>
                    setCreateUserForm({ ...createUserForm, tana_api_key: e.target.value })
                  }
                  className="w-full px-3 py-2 bg-tana-bg border border-tana-border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-1">
                  Node ID (optional)
                </label>
                <input
                  type="text"
                  value={createUserForm.node_id}
                  onChange={(e) =>
                    setCreateUserForm({ ...createUserForm, node_id: e.target.value })
                  }
                  className="w-full px-3 py-2 bg-tana-bg border border-tana-border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="Leave blank for auto-generated Node ID"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 bg-tana-bg text-white rounded-lg hover:bg-white/10 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={actionLoading}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {actionLoading ? 'Creating...' : 'Create User'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Change Password Modal */}
      {showPasswordModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-tana-card border border-tana-border rounded-xl p-6 max-w-md w-full mx-4">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold text-white">Change Password</h3>
              <button
                onClick={() => setShowPasswordModal(false)}
                className="text-tana-muted hover:text-white transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            <form onSubmit={handleChangePassword} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-white mb-1">Username</label>
                <input
                  type="text"
                  value={passwordForm.username}
                  disabled
                  className="w-full px-3 py-2 bg-tana-bg border border-tana-border rounded-lg text-white opacity-50"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-1">New Password</label>
                <input
                  type="password"
                  required
                  value={passwordForm.password}
                  onChange={(e) => setPasswordForm({ ...passwordForm, password: e.target.value })}
                  className="w-full px-3 py-2 bg-tana-bg border border-tana-border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowPasswordModal(false)}
                  className="px-4 py-2 bg-tana-bg text-white rounded-lg hover:bg-white/10 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={actionLoading}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {actionLoading ? 'Updating...' : 'Update Password'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
