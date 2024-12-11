import logging
from rest_framework import status
from quickQrLib.signature_util.signatures import SignatureActions

logger = logging.getLogger(__name__)

class GetRolePermissionsHelper:
    def handle_get_service_permissions(role):
        from permissions_mngmt.models import RolesServicePermissions
        role_service_perms = RolesServicePermissions.get_role_service_permission_by_role(role)
        if role_service_perms:
            return role_service_perms
        else:
            print (f"No service permissions for this role found")
            logger.error(f"No service permissions for this role found")
            return None

    def handle_get_model_permissions(role):
        from permissions_mngmt.models import RolesModelPermissions
        role_model_perms = RolesModelPermissions.get_role_model_permission_by_role(role)
        if role_model_perms:
            return role_model_perms
        else:
            print (f"No model permissions for this role found")
            logger.error(f"No model permissions for this role found")
            return None

# Added User to Role
class AddAppUsersPermissionsHelper:
    def handle_add_service_permissions(role, app_user):
        from permissions_mngmt.serializers import AppUserSignedServicePermissionsCreateSerializer
        print ("\n\n===============================================================\n\n STARTED ADDING SERVICE PERMISSIONS\n\n===============================================================\n\n")
        role_service_perms = GetRolePermissionsHelper.handle_get_service_permissions(role)
        perms_to_add = []
        if role_service_perms:
            for perm in role_service_perms:
                perms_to_add.append({
                    'app_user': app_user,
                    'role': role,
                    'service_permission': perm.service_permission
                })
            if perms_to_add:
                try:
                    signed_permissions, status_code, succeeded = SignatureActions.sign_permissions(perms_to_add)
                    if succeeded:
                        for signed_permission in signed_permissions:
                            signature = signed_permission.pop('signature')
                            service_permission_data = {
                                'service_permission_id': signed_permission['service_permission'].service_permission_id,
                                'service': signed_permission['service_permission'].service.service_id,
                                'name': signed_permission['service_permission'].name,
                                'crud_permissions': signed_permission['service_permission'].crud_permissions
                            }
                            app_user_signed_perm = {
                                'app_user': int(app_user),
                                'service_permission': int(signed_permission['service_permission'].service_permission_id),
                                'service_permission_data': service_permission_data,
                                'service_permission_signature': signature
                            }
                            try:
                                serialized_signed_perm = AppUserSignedServicePermissionsCreateSerializer(data=app_user_signed_perm)
                                if serialized_signed_perm.is_valid():
                                    serialized_signed_perm.save()
                                else:
                                    print (f"\n\nApp Users Signed Service Permissions Serializer Error: {serialized_signed_perm.errors}")
                                    logger.error(f"App Users Signed Service Permissions Serializer Error: {serialized_signed_perm.errors}")
                                    raise Exception(f"App Users Signed Service Permissions Serializer Error: {serialized_signed_perm.errors}")
                            except Exception as e:
                                print (f"\n\nError saving signed permissions: {e}")
                                logger.error(f"Error saving signed permissions: {e}")
                                raise Exception(f"Error saving signed permissions: {e}")
                        return True
                    else:
                        print (f"\n\nError signing permissions: {signed_permissions}")
                        logger.error(f"Error signing permissions: {signed_permissions}")
                        raise Exception(f"Error signing permissions: {signed_permissions}")
                except Exception as e:
                    print (f"\n\nError signing permissions: {e}")
                    logger.error(f"Error signing permissions: {e}")
                    raise Exception(f"Error signing permissions: {e}")
            else:
                print (f"No permissions to add")
                logger.error(f"No permissions to add")
                raise Exception(f"No permissions to add")
        else:
            print (f"No service permissions for this role found")
            logger.error(f"No service permissions for this role found")
            raise Exception(f"No service permissions for this role found")

    def handle_add_model_permissions(role, emp_num):
        from permissions_mngmt.serializers import AppUserSignedModelPermissionsCreateSerializer
        print ("\n\n===============================================================\n\n STARTED ADDING MODEL PERMISSIONS\n\n===============================================================\n\n")
        role_model_perms = GetRolePermissionsHelper.handle_get_model_permissions(role)
        model_perms_to_add = []
        if role_model_perms:
            for perm in role_model_perms:
                model_perms_to_add.append({
                    'model_permission': perm.model_permission,
                    'app_user': emp_num,
                    'role': role
                })
            if model_perms_to_add:
                try:
                    signed_permissions, status_code, succeeded = SignatureActions.sign_permissions(model_perms_to_add)
                    if succeeded:
                        for signed_permission in signed_permissions:
                            # Extracting model_permission fields as JSON serializable data
                            model_permission_data = {
                                'model_permission_id': signed_permission['model_permission'].model_permission_id,
                                'model': signed_permission['model_permission'].model.id,
                                'name': signed_permission['model_permission'].name,
                                'crud_permissions': signed_permission['model_permission'].crud_permissions
                            }
                            signature = signed_permission.pop('signature')
                            app_user_signed_perm = {
                                'app_user': int(emp_num),
                                'model_permission': int(signed_permission['model_permission'].model_permission_id),
                                'model_permission_data': model_permission_data,
                                'model_permission_signature': signature
                            }
                            try:
                                serialized_signed_perm = AppUserSignedModelPermissionsCreateSerializer(data=app_user_signed_perm)
                                if serialized_signed_perm.is_valid():
                                    print (f"\n\nAdded Signed Model Perm\n\nSerialized Signed Permissions: {serialized_signed_perm}")
                                    serialized_signed_perm.save()
                                else:
                                    print (f"\n\nApp Users Signed Model Permissions Serializer Error: {serialized_signed_perm.errors}")
                                    logger.error(f"App Users Signed Model Permissions Serializer Error: {serialized_signed_perm.errors}")
                                    raise Exception(f"App Users Signed Model Permissions Serializer Error: {serialized_signed_perm.errors}")
                            except Exception as e:
                                print (f"\n\nError saving signed permissions: {e}")
                                logger.error(f"Error saving signed permissions: {e}")
                                raise Exception(f"Error saving signed permissions: {e}")
                        return True
                    else:
                        print (f"\n\nError signing permissions: {signed_permissions}")
                        logger.error(f"Error signing permissions: {signed_permissions}")
                        raise Exception(f"Error signing permissions: {signed_permissions}")
                except Exception as e:
                    print (f"\n\nError signing permissions: {e}")
                    logger.error(f"Error signing permissions: {e}")
                    raise Exception(f"Error signing permissions: {e}")
            else:
                print (f"No model permissions to add")
                logger.error(f"No model permissions to add")
                raise Exception(f"No model permissions to add")
        else:
            print (f"No model permissions for this role found")
            logger.error(f"No model permissions for this role found")
            raise Exception(f"No model permissions for this role found")

# Remove User from Role
class RemoveAppUserPermissionsHelper:
    def handle_remove_app_user_service_permissions(old_role, app_user):
        from permissions_mngmt.models import RolesServicePermissions, AppUserServicePermissions
        # return True
        # Get List of Role Service Permissions
        service_perms = RolesServicePermissions.get_role_service_permission_by_role(old_role.role_id)
        if not service_perms:
            print (f"No service permissions for this role found")
            logger.error(f"No service permissions for this role found")
        # Get List of User Service Permissions
        app_user_service_perms = AppUserServicePermissions.get_app_user_service_permission_by_app_user(app_user)
        if not app_user_service_perms:
            print (f"No service permissions for this user found")
            logger.error(f"No service permissions for this user found")
        # Remove User Service Permissions that match Role Service Permissions
        for app_user_perm in app_user_service_perms:
            for role_perm in service_perms:
                if app_user_perm.service == role_perm.service:
                    app_user_perm.delete_employee_service_permission()
        check_app_user_service_perms = AppUserServicePermissions.get_app_user_service_permission_by_app_user(app_user)
        if len(check_app_user_service_perms) == 0:
            return True
        elif len(check_app_user_service_perms) > 0:
            return False

    def handle_remove_app_user_model_permissions(old_role, app_user):
        from permissions_mngmt.models import RolesModelPermissions, AppUsersModelPermissions
        from auth_n_auth.models import AppUserRoles, Roles
        # return True
        role = None
        model_perms = None

        # Get Role for User
        app_user_role = AppUserRoles.get_user_roles_by_app_user(app_user).filter(role=old_role).first()
        if app_user_role:
            print (f"Role for User: {app_user_role}")
            role_for_app_user = app_user_role.role
            role_id = role_for_app_user.role_id
            role = Roles.get_role_by_id(role_id)
            if role:
                # Get List of Role Model Permissions
                model_perms = RolesModelPermissions.get_role_model_permission_by_role(role)
                if model_perms:
                    # Get List of App User Model Permissions
                    app_user_model_perms = AppUsersModelPermissions.get_employee_model_permission_by_employee(app_user)
                    if app_user_model_perms:
                        # Remove Users Model Permissions that match Role Model Permissions
                        for app_user_perm in app_user_model_perms:
                            for role_perm in model_perms:
                                if app_user_perm.model.model_permission_id == role_perm.model_permission_id:
                                    app_user_perm.delete_app_user_model_permission()
                        check_app_user_model_perms = AppUsersModelPermissions.get_app_users_model_permission_by_app_user(app_user)
                        if len(check_app_user_model_perms) == 0:
                            return True
                        elif len(check_app_user_model_perms) > 0:
                            return False

# Deleted Role
class RemoveRolePermissionsHelper:
    # Get List of Users with Role
    def get_app_users_list_by_role(role):
        from auth_n_auth.models import AppUserRoles
        app_users_roles = AppUserRoles.get_user_role_by_role_id(role)
        app_users_list = []
        if app_users_roles:
            for app_user in app_users_roles:
                print (f"User: {app_user.emp_num}")
                app_users_list.append(app_user.emp_num)
            if app_users_list:
                return app_users_list
            else:
                print (f"No users with this role found")
                logger.error(f"No users with this role found")
                return None
        else:
            print (f"No users with this role found")
            logger.error(f"No users with this role found")
            return None

    # Remove Service Permissions for Employees with Role
    def handle_remove_service_permissions(role):
        app_users_in_role = RemoveRolePermissionsHelper.get_app_users_list_by_role(role)

        for app_user in app_users_in_role:
            RemoveAppUserPermissionsHelper.handle_remove_app_user_service_permissions(app_user)

    # Remove Model Permissions for Employees with Role
    def handle_remove_model_permissions(role):
        app_users_in_role = RemoveRolePermissionsHelper.get_app_users_list_by_role(role)

        for app_user in app_users_in_role:
            RemoveAppUserPermissionsHelper.handle_remove_app_user_model_permissions(app_user)

    # Remove Service Permissions for Role
    def handle_remove_service_permssions_for_role(role):
        role_service_perms = GetRolePermissionsHelper.handle_get_service_permissions(role)
        if role_service_perms:
            for perm in role_service_perms:
                perm.delete_role_service_permission()
        else:
            print (f"No service permissions for this role found")
            logger.error(f"No service permissions for this role found")
            return None

    # Remove Model Permissions for Role
    def handle_remove_model_permssions_for_role(role):
        role_model_perms = GetRolePermissionsHelper.handle_get_model_permissions(role)
        if role_model_perms:
            for perm in role_model_perms:
                perm.delete_role_model_permission()
        else:
            print (f"No model permissions for this role found")
            logger.error(f"No model permissions for this role found")
            return None

    def handle_remove_permissions_for_deleted_role(role):
        # Remove Permissions for the Employees with the Deleted Role
        RemoveRolePermissionsHelper.handle_remove_service_permissions(role)
        RemoveRolePermissionsHelper.handle_remove_model_permissions(role)

        # Remove the RoleServicePerms for the Deleted Role
        RemoveRolePermissionsHelper.handle_remove_service_permssions_for_role(role)

        # Remove the RoleModelPerms for the Deleted Role
        RemoveRolePermissionsHelper.handle_remove_model_permssions_for_role(role)

class CheckPermissionsHelper:
    @staticmethod
    def verify_permissions(permission_name, crud_permission, permission=None):
        """
        Verifies if the user has the required permissions.

        Args:
        - user: The user object.
        - permission: The permission object.
        - permission_name: The name of the permission.
        - crud_permission: The CRUD permissions required.
        - special_permission: Optional special permission object.

        Returns:
        - True if the user has the required permissions, False otherwise.
        """
        name_match = permission.get('name') == permission_name
        crud_match = permission.get('crud_permissions') == crud_permission
        if not name_match:
            return False
        if not crud_match:
            return False
        if name_match and crud_match:
            return True
        return None

class GetUserPermissionsHelper:
    @staticmethod
    def get_user_service_permissions(user_id, user_roles):
        from permissions_mngmt.serializers import ServicesPermissionsReadSerializer
        from permissions_mngmt.models import RolesServicePermissions

        service_perms = []
        msg = ""
        status_code = status.HTTP_100_CONTINUE
        if not user_roles:
            print (f"\nNo roles found for user")
            logger.error(f"No roles found for user")
            msg = "No roles found for user"
            status_code = status.HTTP_404_NOT_FOUND
            return msg, status_code, False
        if not user_id:
            print (f"\nNo user id found")
            logger.error(f"No user id found")
            msg = "No user id found"
            status_code = status.HTTP_404_NOT_FOUND
            return msg, status_code, False
        for role_id in user_roles:
            role_service_perms = RolesServicePermissions.get_role_service_permission_by_role(role_id)
            if role_service_perms:
                for perm in role_service_perms:
                    if perm.service_permission not in service_perms:
                        service_perms.append(perm.service_permission)
            else:
                print (f"\nNo service permissions found for role")
                logger.error(f"No service permissions found for role")
                msg = "No service permissions found for role"
                status_code = status.HTTP_404_NOT_FOUND
                return msg, status_code, False
        if not service_perms:
            print (f"\nNo service permissions found for user")
            logger.error(f"No service permissions found for user")
            msg = "No service permissions found for user"
            status_code = status.HTTP_404_NOT_FOUND
            return msg, status_code, False
        else:
            try:
                serialized_service_permissions = ServicesPermissionsReadSerializer(service_perms, many=True)
                return serialized_service_permissions, status.HTTP_200_OK, True
            except Exception as e:
                print (f"\nError serializing service permissions: {e}")
                logger.error(f"Error serializing service permissions: {e}")
                msg = "Error serializing service permissions"
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return msg, status_code, False

    @staticmethod
    def get_user_model_permissions(user_id, user_roles):
        from permissions_mngmt.serializers import ModelsPermissionsReadSerializer
        from permissions_mngmt.models import RolesModelPermissions
        model_perms = []
        msg = ""
        status_code = status.HTTP_100_CONTINUE
        if not user_roles:
            print (f"No roles found for user")
            logger.error(f"No roles found for user")
            msg = "No roles found for user"
            status_code = status.HTTP_404_NOT_FOUND
            return msg, status_code, False
        if not user_id:
            print (f"No user id found")
            logger.error(f"No user id found")
            msg = "No user id found"
            status_code = status.HTTP_404_NOT_FOUND
            return msg, status_code, False
        for role_id in user_roles:
            role_model_perms = RolesModelPermissions.get_role_model_permission_by_role(role_id)
            if role_model_perms:
                for perm in role_model_perms:
                    if perm.model_permission not in model_perms:
                        model_perms.append(perm.model_permission)
            else:
                print (f"No model permissions found for role")
                logger.error(f"No model permissions found for role")
                msg = "No model permissions found for role"
                status_code = status.HTTP_404_NOT_FOUND
                return msg, status_code, False
        if not model_perms:
            print (f"No model permissions found for user")
            logger.error(f"No model permissions found for user")
            msg = "No model permissions found for user"
            status_code = status.HTTP_404_NOT_FOUND
            return msg, status_code, False
        else:
            try:
                serialized_model_permissions = ModelsPermissionsReadSerializer(model_perms, many=True)
                return serialized_model_permissions, status.HTTP_200_OK, True
            except Exception as e:
                print (f"Error serializing model permissions: {e}")
                logger.error(f"Error serializing model permissions: {e}")
                msg = "Error serializing model permissions"
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return msg, status_code, False

# Added User to Role
class AddAppClientUsersPermissionsHelper:
    def handle_add_client_service_permissions(role, app_client_user):
        from permissions_mngmt.serializers import AppClientUserServicePermissionsCreateSerializer
        # return True
        role_service_perms = GetRolePermissionsHelper.handle_get_service_permissions(role)
        perms_to_add = []
        if role_service_perms:
            for perm in role_service_perms:
                perms_to_add.append({
                    'app_client_user': app_client_user,
                    'role': role,
                    'service_permission': perm.service_permission_id
                })
            if perms_to_add:
                serialized_perms = AppClientUserServicePermissionsCreateSerializer(data=perms_to_add, many=True)
                if serialized_perms.is_valid():
                    serialized_perms.save()
                    return True
                else:
                    print (f"\n\nApp Client Users Service Permissions Serializer Error: {serialized_perms.errors}")
                    logger.error(f"App Client Users Service Permissions Serializer Serializer Error: {serialized_perms.errors}")
                    return False
            else:
                print (f"No permissions to add")
                logger.error(f"No permissions to add")
                return False
        else:
            print (f"No service permissions for this role found")
            logger.error(f"No service permissions for this role found")
            return False

    def handle_add_client_model_permissions(role, app_client_user):
        from permissions_mngmt.serializers import AppClientUsersModelPermissionsCreateSerializer
        # return True
        role_model_perms = GetRolePermissionsHelper.handle_get_model_permissions(role)
        model_perms_to_add = []
        if role_model_perms:
            for perm in role_model_perms:
                model_perms_to_add.append({
                    'model_permission': perm.model_permission.model_permission_id,
                    'app_client_user': app_client_user,
                    'role': role
                })
            if model_perms_to_add:
                serialized_model_perms = AppClientUsersModelPermissionsCreateSerializer(data=model_perms_to_add, many=True)
                if serialized_model_perms.is_valid():
                    serialized_model_perms.save()
                    return True
                else:
                    print (f"\n\nApp Client Users Model Permissions Serializer Error: {serialized_model_perms.errors}")
                    logger.error(f"App Client Users Model Permissions Serializer Error: {serialized_model_perms.errors}")
                    return False
            else:
                print (f"No model permissions to add")
                logger.error(f"No model permissions to add")
                return False
        else:
            print (f"No model permissions for this role found")
            logger.error(f"No model permissions for this role found")
            return False

# Remove User from Role
class RemoveAppClientUserPermissionsHelper:
    def handle_remove_app_client_user_service_permissions(old_role, app_client_user):
        from permissions_mngmt.models import RolesServicePermissions, AppClientUserServicePermissions
        # return True
        # Get List of Role Service Permissions
        service_perms = RolesServicePermissions.get_role_service_permission_by_role(old_role)
        if not service_perms:
            print (f"No service permissions for this role found")
            logger.error(f"No service permissions for this role found")
        # Get List of User Service Permissions
        app_user_service_perms = AppClientUserServicePermissions.get_app_client_user_service_permission_by_app_client_user(app_client_user)
        if not app_user_service_perms:
            print (f"No service permissions for this user found")
            logger.error(f"No service permissions for this user found")
        # Remove User Service Permissions that match Role Service Permissions
        for app_user_perm in app_user_service_perms:
            for role_perm in service_perms:
                if app_user_perm.service_permission_id == role_perm.service_permission_id:
                    app_user_perm.delete_app_user_service_permission()
        check_app_user_service_perms = AppClientUserServicePermissions.get_app_client_user_service_permission_by_app_client_user(app_client_user)
        if len(check_app_user_service_perms) == 0:
            return True
        elif len(check_app_user_service_perms) > 0:
            return False

    def handle_remove_app_client_user_model_permissions(old_role, app_client_user):
        from permissions_mngmt.models import RolesModelPermissions, AppClientUsersModelPermissions
        from auth_n_auth.models import AppClientUserRoles, Roles
        # return True
        role = None
        model_perms = None
        # Get Role for User
        app_client_user_role = AppClientUserRoles.get_client_user_roles_by_app_client_user(app_client_user).filter(role=old_role).first()
        if app_client_user_role:
            print (f"Role for User: {app_client_user_role}")
            role_for_app_client_user = app_client_user_role.role
            role_id = role_for_app_client_user.role_id
            role = Roles.get_role_by_id(role_id)
            if role:
                # Get List of Role Model Permissions
                model_perms = RolesModelPermissions.get_role_model_permission_by_role(role)
                if model_perms:
                    # Get List of App User Model Permissions
                    app_user_model_perms = AppClientUsersModelPermissions.get_app_client_users_model_permission_by_app_client_user(app_client_user)
                    if app_user_model_perms:
                        # Remove Users Model Permissions that match Role Model Permissions
                        for app_user_perm in app_user_model_perms:
                            for role_perm in model_perms:
                                if app_user_perm.model_permission_id == role_perm.model_permission_id:
                                    app_user_perm.delete_app_client_user_model_permission()
                        check_app_user_model_perms = AppClientUsersModelPermissions.get_app_client_users_model_permission_by_app_client_user(app_client_user)
                        if len(check_app_user_model_perms) == 0:
                            return True
                        elif len(check_app_user_model_perms) > 0:
                            return False
