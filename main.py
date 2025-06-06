from database import (
    check_database,
    create_user_table,
    add_user,
    login_user,
    list_users,
    delete_user_by_id
)

def admin_menu():
    while True:
        print("\n--- Menú Administrador ---")
        print("1. Ver usuarios")
        print("2. Eliminar usuario")
        print("0. Cerrar sesión")
        option = input("Opción: ")
        if option == "1":
            list_users()
            input("Presiona ENTER para continuar...")
        elif option == "2":
            user_id = input("Ingrese el ID del usuario a eliminar: ")
            if not user_id.isdigit():
                print(" ID inválido.")
            else:
                delete_user_by_id(user_id)
            input("Presiona ENTER para continuar...")
        elif option == "0":
            break
        else:
            print(" Opción inválida.")

def user_menu(name):
    print(f"\n Bienvenido/a {name}. No tienes permisos administrativos.")
    input("Presiona ENTER para cerrar sesión.")

def main_menu():
    check_database()
    create_user_table()

    while True:
        print("\n=== Sistema de Gestión de Usuarios ===")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("0. Salir")
        option = input("Seleccione una opción: ")

        if option == "1":
            full_name = input("Nombre completo: ")
            username = input("Nombre de usuario: ")
            password = input("Contraseña: ")
            role = input("Rol (admin/usuario): ").lower()
            add_user(full_name, username, password, role)
        elif option == "2":
            username = input("Usuario: ")
            password = input("Contraseña: ")
            user = login_user(username, password)
            if user:
                if user["role"] == "admin":
                    admin_menu()
                else:
                    user_menu(user["name"])
            else:
                print("Usuario o contraseña incorrectos.")
        elif option == "0":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main_menu()
