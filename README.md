# Password Manager - Shared PostgreSQL Backend

This project sets up a publicly accessible PostgreSQL database using Docker to serve as the backend for a password manager. The container is hosted on a virtual machine and can be accessed remotely via `psql` by authorized users.

---

## Repository

GitHub: [https://github.com/rollaxse/project_4](https://github.com/rollaxse/project_4)

---

## Use Case

This database is designed to store **user credentials, vault items, and encryption-related metadata** for a password manager application (currently in development or testing phase). Multiple developers can connect to this shared database for collaborative testing and development.

---

## Connection Details (for Developers)

Connect via the `psql` CLI using the following credentials:

| Field | Value |
|--------------|-------------------|
| **Host** | `192.168.12.114` |
| **Port** | `5432` |
| **Username** | `postgres` |
| **Password** | `docker` |
| **Database** | `world` |

---

## How to Connect via `psql`

From any machine with the PostgreSQL client installed:

```bash
psql -h 192.168.12.114 -p 5432 -U postgres -d world
