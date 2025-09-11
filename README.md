# backend-horarios
 codex/generate-hasheada-password-and-update-demo_seed.sql
## Demo credentials

The development database includes an initial administrative user for testing:

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | `admin`  | `admin123` |

Use these credentials to sign in during demos.
=======
## Disponibilidad de Docentes

- **Disponibilidad registrada**: bloques de tiempo que el docente ha indicado como aptos para impartir clases.
- **Tiempos libres calculados**: huecos sin clases encontrados automáticamente en el horario del docente.

La disponibilidad registrada puede no coincidir con los tiempos libres calculados. Un docente puede tener
tiempos libres en su horario que no haya marcado como disponibles, o viceversa.

## Campos de auditoría

Los modelos `Docente`, `Materia`, `AsignacionMateria` y `ClaseProgramada` ahora incluyen los campos
`created_at` y `updated_at` proporcionados por `TimestampMixin`. Estos campos registran la fecha de creación
del registro y se actualizan automáticamente al modificarlo.
 main

