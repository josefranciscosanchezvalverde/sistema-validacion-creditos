from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import Credito
import os

# =========================
# LOGIN
# =========================
@never_cache
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('panel_admin')
            else:
                return redirect('portal_estudiante')
    return render(request, 'login.html')

# =========================
# REGISTRO
# =========================
@never_cache
def registro_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_completo', '').strip()
        correo = request.POST.get('correo', '').strip()
        matricula = request.POST.get('matricula', '').strip()
        password = request.POST.get('password', '')

        if not nombre or not correo or not matricula or not password:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'registro.html')

        correo_correcto = f"{matricula}@teschi.edu.mx"
        if correo.lower() != correo_correcto.lower():
            messages.error(request, f'El correo debe ser: {correo_correcto}')
            return render(request, 'registro.html')

        if User.objects.filter(email=correo).exists():
            messages.error(request, 'El correo ya está registrado.')
            return render(request, 'registro.html')

        if User.objects.filter(username=matricula).exists():
            messages.error(request, 'La matrícula ya existe.')
            return render(request, 'registro.html')

        User.objects.create_user(
            username=matricula,
            email=correo,
            password=password,
            first_name=nombre
        )
        messages.success(request, 'Usuario creado correctamente.')
        return redirect('login')

    return render(request, 'registro.html')

# =========================
# PORTAL ESTUDIANTE
# =========================
@login_required(login_url='login')
@never_cache
def portal_estudiante_view(request):
    if request.method == 'POST':
        numero = request.POST.get('numero_credito')
        semestre = request.POST.get('semestre')
        archivo = request.FILES.get('documento_pdf')

        if numero and semestre and archivo:
            creditos = Credito.objects.filter(alumno=request.user, numero_credito=numero)
            for c in creditos:
                try:
                    if c.archivo and os.path.exists(c.archivo.path):
                        os.remove(c.archivo.path)
                except Exception as e:
                    print("Error borrando archivo:", e)
            creditos.delete()
            Credito.objects.create(
                alumno=request.user, numero_credito=numero, semestre=semestre,
                archivo=archivo, estado='En Revisión'
            )
            return redirect('portal_estudiante')

    creditos_usuario = Credito.objects.filter(alumno=request.user)
    dict_creditos = {c.numero_credito: c for c in creditos_usuario}
    lista = []
    for i in range(1, 6):
        if i in dict_creditos:
            c = dict_creditos[i]
            lista.append({
                'numero': i, 'subido': True, 'estado': c.estado,
                'archivo_nombre': os.path.basename(c.archivo.name) if c.archivo else 'Documento.pdf',
                'semestre': c.semestre, 'fecha': c.fecha_subida.strftime('%d/%m/%Y') if hasattr(c, 'fecha_subida') else '---'
            })
        else:
            lista.append({'numero': i, 'subido': False, 'estado': 'Sin subir'})

    aprobados = creditos_usuario.filter(estado='Aprobado').count()
    contexto = {
        'nombre_estudiante': request.user.first_name, 'matricula': request.user.username,
        'lista_creditos': lista, 'creditos_aprobados': aprobados, 'creditos_faltantes': 5 - aprobados
    }
    return render(request, 'portal_estudiante.html', contexto)

# =========================
# LOGOUT
# =========================
def salir_view(request):
    logout(request)
    return redirect('login')

# =========================
# PANEL ADMIN
# =========================
@login_required(login_url='login')
@never_cache
def panel_admin_view(request):
    if not request.user.is_superuser:
        return redirect('portal_estudiante')

    estudiantes = User.objects.filter(is_superuser=False)
    datos = []
    total_docs = 0
    total_revision = 0
    total_aprobados = 0

    for est in estudiantes:
        creds = Credito.objects.filter(alumno=est)
        total_docs += creds.count()
        total_revision += creds.filter(estado='En Revisión').count()
        total_aprobados += creds.filter(estado='Aprobado').count()
        datos.append({'estudiante': est, 'creditos': creds, 'total_aprobados': creds.filter(estado='Aprobado').count()})

    contexto = {
        'datos_estudiantes': datos, 'total_estudiantes': estudiantes.count(),
        'total_documentos': total_docs, 'total_en_revision': total_revision,
        'total_aprobados_global': total_aprobados
    }
    return render(request, 'admin_panel.html', contexto)

# =========================
# APROBAR CRÉDITO
# =========================
@login_required(login_url='login')
@never_cache
def aprobar_credito(request, credito_id):
    if not request.user.is_superuser:
        return redirect('portal_estudiante')
    credito = get_object_or_404(Credito, id=credito_id)
    if credito.estado != 'Aprobado':
        credito.estado = 'Aprobado'
        credito.save()
    return redirect('panel_admin')

# =========================
# RECHAZAR CRÉDITO
# =========================
@login_required(login_url='login')
@never_cache
def rechazar_credito(request, credito_id):
    if not request.user.is_superuser:
        return redirect('portal_estudiante')
    credito = get_object_or_404(Credito, id=credito_id)
    credito.estado = 'Rechazado'
    credito.save()
    return redirect('panel_admin')

# =========================
# GESTIÓN DE ADMINISTRADORES
# =========================
@login_required(login_url='login')
@never_cache
def gestion_administradores_view(request):
    if not request.user.is_superuser:
        return redirect('portal_estudiante')

    if request.method == 'POST':
        usuario = request.POST.get('usuario', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip()
        password = request.POST.get('password', '')

        if not usuario or not nombre or not correo or not password:
            messages.error(request, 'Todos los campos son obligatorios.')
        elif User.objects.filter(username=usuario).exists():
            messages.error(request, 'Ese Usuario ya está en uso.')
        elif User.objects.filter(email=correo).exists():
            messages.error(request, 'Ese correo ya está registrado.')
        else:
            try:
                user = User.objects.create_user(username=usuario, email=correo, password=password, first_name=nombre)
                user.is_staff = True
                user.is_superuser = True 
                user.save()
                messages.success(request, 'Administrador creado con éxito.')
                return redirect('gestion_administradores')
            except Exception as e:
                messages.error(request, f'Error al crear: {e}')

    administradores = User.objects.filter(is_superuser=True)
    return render(request, 'gestion_administradores.html', {'administradores': administradores})

# =========================
# RESETEAR CONTRASEÑA ADMIN
# =========================
@login_required(login_url='login')
@never_cache
def resetear_password_admin(request):
    if not request.user.is_superuser:
        return redirect('portal_estudiante')

    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        nueva_password = request.POST.get('nueva_password')
        confirmar_password = request.POST.get('confirmar_password')
        admin_user = get_object_or_404(User, id=admin_id)

        if admin_user == request.user:
            messages.error(request, 'No puedes resetear tu propia contraseña desde aquí.')
        elif nueva_password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            admin_user.set_password(nueva_password)
            admin_user.save()
            messages.success(request, f'Contraseña de {admin_user.first_name or admin_user.username} actualizada.')

    return redirect('gestion_administradores')

# =========================
# ELIMINAR ESTUDIANTE
# =========================
@login_required(login_url='login')
@never_cache
def eliminar_estudiante(request, id):
    if not request.user.is_superuser:
        return redirect('portal_estudiante')
    
    estudiante = get_object_or_404(User, id=id)
    estudiante.delete()
    messages.success(request, f'El estudiante {estudiante.first_name} ha sido eliminado.')
    return redirect('panel_admin')