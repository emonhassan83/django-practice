# Tailwind CSS in Django — Short Guideline

Ei project-e Tailwind CSS v4 CLI use kora hoyeche. Tailwind template gula scan kore, je class use hoyeche shudhu shegula diye ekta CSS file (`static/css/output.css`) banay. Django oi file ta normal static file hishebe serve kore.

## Folder structure

```
django-practice/
├── package.json            # npm scripts (build:css, watch:css)
├── static/
│   ├── src/input.css       # Tailwind source (edit this)
│   ├── css/output.css      # Generated file (do not edit)
│   ├── css/index.css       # Custom plain CSS
│   ├── js/main.js
│   └── images/logo.svg
└── tasks/templates/        # Tailwind scans these files
```



## Step 1: Django static settings

`task_management/settings.py`-e `django.contrib.staticfiles` `INSTALLED_APPS`-e thakte hobe, ar project-er `static` folder register korte hobe:

```python
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```



## Step 2: Tailwind install

Node.js lagbe (v18+). Project root-e:

```bash
npm init -y
npm install -D tailwindcss @tailwindcss/cli
```

`node_modules/` `.gitignore`-e add koro.

## Step 3: Input CSS banao

`static/src/input.css`:

```css
@import "tailwindcss";

/* Kon folder-er template scan korbe */
@source "../../tasks/templates";
```

Notun app-er template folder add korle (jemon `users/templates`), oitar jonno arekta `@source` line add koro.

Custom color/font `@theme`-e, ar reusable class `@layer components`-e `@apply` diye likho:

```css
@theme {
  --color-brand-600: #4f46e5;
}

@layer components {
  .btn-primary {
    @apply px-4 py-2.5 rounded-lg text-white bg-brand-600;
  }
}
```



## Step 4: npm scripts

`package.json`:

```json
"scripts": {
  "build:css": "tailwindcss -i ./static/src/input.css -o ./static/css/output.css --minify",
  "watch:css": "tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch"
}
```



## Step 5: Template-e CSS load koro

Template-er ekdom upore `{% load static %}` dao, tarpor `<head>`-e:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/output.css' %}">
<link rel="stylesheet" href="{% static 'css/index.css' %}">
```

Template inheritance use korle shudhu base template-e (`dashboard/dashboard.html`) dilei hobe; child template gula automatically pabe.

## Step 6: Development-e run koro

Duita terminal lagbe:

```bash
# Terminal 1: Tailwind watch (template save korlei CSS rebuild hobe)
npm run watch:css

# Terminal 2: Django server
python manage.py runserver
```

Production/deploy-er age:

```bash
npm run build:css
python manage.py collectstatic
```



## Common problems

- **Notun class kaj korche na**: `watch:css` cholche kina dekho, ba `npm run build:css` abar chalao. Template folder `@source`-e ache kina check koro.
- **Dynamic class name** (jemon `"bg-" + color`) Tailwind dhorte pare na. Class name puro likho, jemon `bg-red-500`.
- **Browser purono CSS dekhacche**: hard refresh koro (`Ctrl + Shift + R`).
- `output.css` **hand-edit koro na**: proti build-e overwrite hoye jabe. Change `input.css`-e koro.

