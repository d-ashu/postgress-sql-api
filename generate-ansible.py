def generate_ansible(max_connections, shared_buffers, postgres_version=12):
    playbook_content = f"""
---
- hosts: all
  become: yes
  vars:
    postgres_version: {postgres_version}

  tasks:
    - name: Install PostgreSQL
      apt:
        name: "postgresql-{{ postgres_version }}"
        state: present
        update_cache: yes

    - name: Configure PostgreSQL settings
      lineinfile:
        path: "/etc/postgresql/{{ postgres_version }}/main/postgresql.conf"
        regexp: '^#?(max_connections|shared_buffers) ='
        line: "{{{{ item }}}}"
        state: present
      with_items:
        - "max_connections = {max_connections}"
        - "shared_buffers = {shared_buffers}"

    - name: Restart PostgreSQL service
      service:
        name: postgresql
        state: restarted
    """

    # Write the playbook content to configure_postgres.yml
    with open("configure_postgres.yml", "w") as f:
        f.write(playbook_content)

    print("Ansible playbook 'configure_postgres.yml' generated successfully.")

# Run the function with example values
if __name__ == "__main__":
    generate_ansible(max_connections=100, shared_buffers="256MB")