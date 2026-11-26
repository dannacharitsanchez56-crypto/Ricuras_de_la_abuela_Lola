
from django.core.signing import TimestampSigner, BadSignature
from django.urls import reverse
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET, require_POST
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
from io import BytesIO
from .models import Plato, Venta, RegistroVenta, Resena
from .forms import PlatoForm, ResenaForm
from .decorators import solo_staff
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from .models import OpcionesAlmuerzo, PedidoConEleccion
from .personalizacion_forms import (OpcionesAlmuerzoForm,ElegirAlmuerzoForm)
from django.http import Http404
from urllib.parse import quote
from django.db import transaction
from django.db.models import Sum, Count, Q
from decimal import Decimal, InvalidOperation


def portada(request):
    return render(request, 'portada.html')


def inicio(request):
    contexto = {
        'metodos': [
            {'nombre': 'Nequi', 'icono': '📱'},
            {'nombre': 'Efectivo', 'icono': '💵'},
            {'nombre': 'Bancolombia', 'icono': '🏦'},
        ]
    }
    return render(request, 'inicio.html', contexto)


def menu(request):
    platos = Plato.objects.all().order_by('-disponible', 'nombre')
    return render(request, 'menu.html', {'platos': platos})


def contacto(request):
    contexto = {
        'metodos': [
            {'nombre': 'Nequi', 'icono': '📱'},
            {'nombre': 'Efectivo', 'icono': '💵'},
            {'nombre': 'Bancolombia', 'icono': '🏦'},
        ]
    }
    return render(request, 'contacto.html', contexto)


@login_required
def perfil(request):
    return render(request, 'perfil.html')


# AQUÍ QUITAMOS EL @solo_staff PARA QUE SE VEA LA PÁGINA
def Platos(request):
    platos = Plato.objects.all()
    return render(request, 'Platos.html', {'platos': platos})


def plato_detalle(request, id):
    plato = get_object_or_404(Plato, id=id)
    lista_resenas = plato.resena_set.all()

    prom = lista_resenas.aggregate(Avg('estrellas'))['estrellas__avg']

    mi_resena = None
    if request.user.is_authenticated:
        mi_resena = Resena.objects.filter(
            plato=plato, usuario=request.user
        ).first()

    if request.method == 'POST':
        if request.user.is_authenticated:
            if mi_resena:
                form = ResenaForm(request.POST, instance=mi_resena)
            else:
                form = ResenaForm(request.POST)

            if form.is_valid():
                r = form.save(commit=False)
                r.plato = plato
                r.usuario = request.user
                r.save()
                return redirect('plato_detalle', id=plato.id)
        else:
            return redirect('login')
    else:
        if mi_resena:
            form = ResenaForm(instance=mi_resena)
        else:
            form = ResenaForm()

    contexto = {
        'plato': plato,
        'resenas': lista_resenas,
        'form': form,
        'promedio': prom,
        'mi_resena': mi_resena
    }
    return render(request, 'plato_detalle.html', contexto)


@solo_staff
def crear_plato(request):

    form = PlatoForm(
        request.POST or None,
        request.FILES or None
    )

    opciones_form = OpcionesAlmuerzoForm(
        request.POST or None,
        prefix='opciones'
    )

    if request.method == 'POST':

        if form.is_valid() and opciones_form.is_valid():

            if form.cleaned_data.get('personalizable'):

                for campo in [
                    'proteinas',
                    'principios',
                    'acompanamientos'
                ]:
                    if not opciones_form.cleaned_data[campo]:
                        opciones_form.add_error(
                            campo,
                            'Selecciona al menos una opción.'
                        )

            if not opciones_form.errors:

                plato = form.save()

                opciones = opciones_form.save(commit=False)
                opciones.plato = plato
                opciones.save()

                messages.success(
                    request,
                    'Plato creado correctamente.'
                )

                return redirect('Platos')

        messages.error(
            request,
            'Revisa los campos del formulario.'
        )

    return render(request, 'plato_form.html', {
        'form': form,
        'opciones_form': opciones_form,
        'titulo': 'Agregar plato',
        'boton_texto': 'Guardar plato',
    })



@solo_staff
def editar_plato(request, id):

    plato = get_object_or_404(Plato, id=id)

    configuracion = OpcionesAlmuerzo.objects.filter(
        plato=plato
    ).first()

    form = PlatoForm(
        request.POST or None,
        request.FILES or None,
        instance=plato
    )

    opciones_form = OpcionesAlmuerzoForm(
        request.POST or None,
        instance=configuracion,
        prefix='opciones'
    )

    if request.method == 'POST':

        if form.is_valid() and opciones_form.is_valid():

            if form.cleaned_data.get('personalizable'):

                for campo in [
                    'proteinas',
                    'principios',
                    'acompanamientos'
                ]:
                    if not opciones_form.cleaned_data[campo]:
                        opciones_form.add_error(
                            campo,
                            'Selecciona al menos una opción.'
                        )

            if not opciones_form.errors:

                form.save()

                opciones = opciones_form.save(commit=False)
                opciones.plato = plato
                opciones.save()

                messages.success(
                    request,
                    'Plato actualizado correctamente.'
                )

                return redirect('Platos')

        messages.error(
            request,
            'Revisa los campos del formulario.'
        )

    return render(request, 'plato_form.html', {
        'form': form,
        'opciones_form': opciones_form,
        'plato': plato,
        'titulo': 'Editar plato',
        'boton_texto': 'Guardar cambios',
    })



@solo_staff
def eliminar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == 'POST':
        plato.delete()
        messages.success(request, 'Plato eliminado correctamente.')
        return redirect('Platos')
    return render(request, 'plato_confirmar_eliminar.html', {'plato': plato})


@solo_staff
def eliminar_resena(request, resena_id):
    r = get_object_or_404(Resena, id=resena_id)
    plato_id = r.plato.id

    r.delete()
    messages.success(request, 'Reseña eliminada.')

    return redirect('plato_detalle', id=plato_id)



def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password1 or not password2:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'registro.html')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')

        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'registro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya está en uso.')
            return render(request, 'registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ese correo electrónico ya está registrado.')
            return render(request, 'registro.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.save()
            messages.success(
                request,
                '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.'
            )
            return redirect('login')
        except Exception as e:
            messages.error(
                request,
                f'Ocurrió un error al crear la cuenta: {str(e)}'
            )
            return render(request, 'registro.html')

    return render(request, 'registro.html')



@staff_member_required
def resumen_ventas(request):

    ventas = RegistroVenta.objects.all().order_by('-fecha')

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio:
        ventas = ventas.filter(fecha__date__gte=fecha_inicio)

    if fecha_fin:
        ventas = ventas.filter(fecha__date__lte=fecha_fin)

    resumen = ventas.aggregate(
        total_vendido=Sum('total'),
        cantidad_ventas=Count('id'),
        platos_vendidos=Sum('cantidad'),
        ventas_web=Count('id', filter=Q(origen='web'))
    )

    contexto = {
        'ventas': ventas,
        'total_vendido': resumen['total_vendido'] or 0,
        'cantidad_ventas': resumen['cantidad_ventas'],
        'platos_vendidos': resumen['platos_vendidos'] or 0,
        'ventas_web': resumen['ventas_web'],
        'fecha_inicio': fecha_inicio or '',
        'fecha_fin': fecha_fin or '',
    }

    return render(request, 'resumen_ventas.html', contexto)


@staff_member_required
def registrar_venta(request):
    if request.method == 'POST':

        try:
            monto = Decimal(request.POST.get('monto', ''))
            cantidad = int(request.POST.get('cantidad', ''))

            if not monto.is_finite() or monto <= 0 or cantidad <= 0:
                messages.error(
                    request,
                    'Ingresa valores mayores que cero.'
                )
                return redirect('registrar_venta')

            venta = RegistroVenta.objects.create(
                total=monto,
                cantidad=cantidad,
                origen='manual'
            )

            if request.POST.get('descargar_excel') == 'on':
                return _crear_excel_ventas(
                    RegistroVenta.objects.filter(pk=venta.pk),
                    f'venta_{venta.pk}.xlsx'
                )

            messages.success(
                request,
                f'Venta registrada: {cantidad} platos vendidos.'
            )

            return redirect('resumen_ventas')

        except (InvalidOperation, ValueError):
            messages.error(request, 'Ingresa valores válidos.')
            return redirect('registrar_venta')

    return render(request, 'registrar_venta.html')


def _crear_excel_ventas(ventas, nombre_archivo):
    wb = Workbook()
    ws = wb.active
    ws.title = "Ventas"

    encabezados = [
        "ID", 
        "Fecha", 
        "Hora", 
        "Cantidad de platos",
        "Origen",
        "Total (COP)"]
    ws.append([
        venta.id,
        fecha.strftime("%d/%m/%Y"),
        fecha.strftime("%H:%M"),
        venta.cantidad,
        venta.get_origen_display(),
        float(venta.total)
    ])

    for celda in ws[1]:
        celda.font = Font(
            bold=True,
            color="FFFFFF"
        )
        celda.fill = PatternFill(
            start_color="8B4513",
            end_color="8B4513",
            fill_type="solid"
        )
        celda.alignment = Alignment(
            horizontal="center"
        )

    for venta in ventas:
        fecha = timezone.localtime(venta.fecha) if timezone.is_aware(venta.fecha) else venta.fecha

        ws.append([
            venta.id,
            fecha.strftime("%d/%m/%Y"),
            fecha.strftime("%H:%M"),
            venta.cantidad,
            venta.get_origen_display(),
            float(venta.total)
        ])

    for fila in ws.iter_rows(min_row=2):
        fila[5].number_format = '"$"#,##0.00'

    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 15
    ws.column_dimensions["D"].width = 25
    ws.column_dimensions["E"].width = 20
    ws.column_dimensions["F"].width = 22

    archivo = BytesIO()
    wb.save(archivo)
    archivo.seek(0)

    respuesta = HttpResponse(
        archivo.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    respuesta["Content-Disposition"] = (
        f'attachment; filename="{nombre_archivo}"'
    )

    return respuesta

@staff_member_required
@require_GET
def exportar_ventas_excel(request):
    ventas = RegistroVenta.objects.all().order_by("-fecha")

    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    if fecha_inicio:
        ventas = ventas.filter(fecha__date__gte=fecha_inicio)

    if fecha_fin:
        ventas = ventas.filter(fecha__date__lte=fecha_fin)

    return _crear_excel_ventas(
        ventas,
        "reporte_ventas.xlsx"
    )

@staff_member_required
@require_GET
def descargar_venta_excel(request, venta_id):
    ventas = RegistroVenta.objects.filter(id=venta_id)

    return _crear_excel_ventas(
        ventas,
        f"venta_{venta_id}.xlsx"
    )


# PERSONALIZACIÓN DEL ALMUERZO
# Esta vista permite pedidos sin iniciar sesión.

def personalizar_almuerzo(request, id):

    plato = get_object_or_404(
        Plato,
        id=id,
        personalizable=True,
        disponible=True
    )

    configuracion = OpcionesAlmuerzo.objects.filter(
        plato=plato
    ).first()

    if not configuracion or not all([
        configuracion.proteinas,
        configuracion.principios,
        configuracion.acompanamientos
    ]):
        messages.error(
            request,
            'Este almuerzo todavía no tiene opciones configuradas.'
        )
        return redirect('menu')

    form = ElegirAlmuerzoForm(
        request.POST or None,
        configuracion=configuracion
    )

    if request.method == 'POST' and form.is_valid():
        pedido = PedidoConEleccion.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            plato=plato,
            nombre_plato=plato.nombre,
            proteina=form.cleaned_data['proteina'],
            principio=form.cleaned_data['principio'],
            acompanamiento=form.cleaned_data['acompanamiento'],
            precio=plato.precio
        )

        # Enlace seguro que permite consultar el pedido sin iniciar sesión
        firmador = TimestampSigner(
            salt='ricuras-pedido-personalizado'
        )
        token = firmador.sign(str(pedido.id))
        url = reverse('pedido_personalizado', args=[pedido.id])
        enlace = f"{url}?{urlencode({'token': token})}"

        return HttpResponseRedirect(enlace)

    return render(
        request,
        'personalizar_almuerzo.html',
        {
            'plato': plato,
            'form': form
        }
    )


# RESUMEN DEL PEDIDO PERSONALIZADO
# El cliente puede entrar mediante su enlace seguro.

def pedido_personalizado(request, id):

    pedido = get_object_or_404(
        PedidoConEleccion,
        id=id
    )

    es_propietario = (
        request.user.is_authenticated
        and pedido.usuario_id == request.user.id
    )

    # Un visitante accede mediante el token firmado del enlace.
    token = request.GET.get('token', '')
    token_valido = False

    if token:
        firmador = TimestampSigner(
            salt='ricuras-pedido-personalizado'
        )
        try:
            id_firmado = firmador.unsign(
                token,
                max_age=7 * 24 * 60 * 60
            )
            token_valido = (id_firmado == str(pedido.id))
        except BadSignature:
            token_valido = False

    if not es_propietario and not token_valido:
        raise Http404('Pedido no encontrado')

    precio_formateado = f"{pedido.precio:,.0f}".replace(',', '.')
    cliente = (
        pedido.usuario.username
        if pedido.usuario_id
        else 'Cliente invitado'
    )

    mensaje = (
        "Hola, quiero realizar un pedido en "
        "Ricuras de la Abuela Lola.\n\n"
        f"Pedido #{pedido.id}\n"
        f"Plato: {pedido.nombre_plato}\n\n"
        "Mi almuerzo personalizado:\n"
        f"Proteína: {pedido.proteina}\n"
        f"Principio: {pedido.principio}\n"
        f"Acompañamiento: {pedido.acompanamiento}\n\n"
        f"Total: ${precio_formateado} COP\n"
        f"Cliente: {cliente}\n\n"
        "Quisiera confirmar mi pedido. ¡Gracias!"
    )

    numero_whatsapp = '573118299494'
    whatsapp_url = (
        f'https://wa.me/{numero_whatsapp}'
        f'?text={quote(mensaje)}'
    )

    return render(
        request,
        'pedido_personalizado.html',
        {
            'pedido': pedido,
            'whatsapp_url': whatsapp_url
        }
    )


# PANEL ADMINISTRATIVO DE PEDIDOS PERSONALIZADOS

@staff_member_required(login_url='login')
def pedidos_recibidos(request):
    pedidos = PedidoConEleccion.objects.select_related(
        'usuario'
    ).order_by('-fecha')

    estados = PedidoConEleccion.ESTADOS
    estado_actual = request.GET.get('estado', '')
    estados_validos = [valor for valor, nombre in estados]

    if estado_actual in estados_validos:
        pedidos = pedidos.filter(estado=estado_actual)

    return render(
        request,
        'pedidos_recibidos.html',
        {
            'pedidos': pedidos,
            'estados': estados,
            'estado_actual': estado_actual
        }
    )

@staff_member_required(login_url='login')
@require_POST
@transaction.atomic
def cambiar_estado_pedido(request, id):

    pedido = get_object_or_404(PedidoConEleccion, id=id)

    nuevo_estado = request.POST.get('estado', '')

    estados_validos = [
        valor for valor, nombre in PedidoConEleccion.ESTADOS
    ]

    if nuevo_estado not in estados_validos:
        messages.error(request, 'El estado no es válido.')
        return redirect('pedidos_recibidos')

    pedido.estado = nuevo_estado
    pedido.save(update_fields=['estado'])

    if nuevo_estado == 'pagado':

        actualizado = PedidoConEleccion.objects.filter(
            pk=pedido.pk,
            venta_registrada=False
        ).update(venta_registrada=True)

        if actualizado:
            RegistroVenta.objects.create(
                total=pedido.precio,
                cantidad=1,
                origen='web'
            )

            messages.success(
                request,
                'Almuerzo registrado automáticamente en ventas.'
            )

    messages.success(
        request,
        f'Pedido #{pedido.id} actualizado correctamente.'
    )

    return redirect('pedidos_recibidos')

@staff_member_required
@require_POST
def eliminar_venta(request, venta_id):

    venta = get_object_or_404(
        RegistroVenta,
        id=venta_id
    )

    if venta.origen == 'web':
        messages.error(
            request,
            'Las ventas web deben gestionarse desde los pedidos.'
        )
        return redirect('resumen_ventas')

    venta.delete()

    messages.success(
        request,
        'Venta eliminada correctamente.'
    )

    return redirect('resumen_ventas')

@staff_member_required
def editar_venta(request, venta_id):

    venta = get_object_or_404(
        RegistroVenta,
        id=venta_id
    )

    if venta.origen != 'manual':
        messages.error(
            request,
            'No puedes editar directamente una venta web.'
        )
        return redirect('resumen_ventas')

    if request.method == 'POST':

        try:
            cantidad = int(request.POST.get('cantidad', ''))
            monto = Decimal(request.POST.get('monto', ''))

            if (
                cantidad <= 0
                or not monto.is_finite()
                or monto <= 0
            ):

                messages.error(
                    request,
                    'Ingresa valores mayores que cero.'
                )

                return redirect('editar_venta', venta_id=venta.id)

            venta.cantidad = cantidad
            venta.total = monto

            venta.full_clean()

            venta.save(update_fields=['cantidad', 'total'])

            messages.success(
                request,
                'Venta actualizada correctamente.'
            )

            return redirect('resumen_ventas')

        except (InvalidOperation, ValueError, ValidationError):

            messages.error(
                request,
                'Ingresa una cantidad y un monto válidos.'
            )

            return redirect('editar_venta', venta_id=venta.id)

    return render(
        request,
        'editar_venta.html',
        {
            'venta': venta
        }
    )