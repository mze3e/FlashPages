---
title: "Component Guide"
slug: "components"
layout: "docs"
description: "Complete guide to using shorthand components in your content"
nav_order: 5
---

# Component System Guide

This guide shows you how to use our powerful component system with simple shorthand notation.

## Getting Started

Components use a simple bracket syntax:
```markdown
[component_type parameter="value" another_param="value"]
```

## Available Components

### Hero Section
Create stunning hero sections with background images and call-to-action buttons:

```markdown
[hero title="Your Title" subtitle="Your subtitle" bg_image="image-url" button_text="Click Me" button_url="link" button_color="primary"]
```

**Parameters:**
- `title` - Main heading text
- `subtitle` - Subheading text (optional)
- `bg_image` - Background image URL
- `button_text` - Button text
- `button_url` - Button link OR `modal_target` for modal
- `button_color` - Bootstrap color (primary, secondary, success, etc.)

### Cards
Create responsive card layouts:

```markdown
[card title="Card Title" text="Card description" image="image-url" button_text="Action" button_url="link" width="4"]
```

**Parameters:**
- `title` - Card title
- `text` - Card description
- `image` - Card image URL (optional)
- `button_text` - Button text (optional)
- `button_url` - Button link OR `modal_target`
- `button_color` - Button style
- `width` - Bootstrap column width (1-12)

### Call-to-Action (CTA)
Eye-catching CTA sections:

```markdown
[cta title="Take Action Now" subtitle="Don't miss this opportunity" button_text="Get Started" modal_target="signupModal" bg_color="primary"]
```

### Features
Highlight key features with icons:

```markdown
[feature icon="rocket" title="Fast Performance" text="Lightning-fast loading times" icon_color="primary" width="4"]
```

### Testimonials
Customer testimonials with photos:

```markdown
[testimonial author="John Doe" company="Acme Corp" quote="Amazing product!" image="author-photo-url" width="6"]
```

### Pricing Cards
Professional pricing tables:

```markdown
[pricing title="Pro Plan" price="99" period="month" features="Feature 1,Feature 2,Feature 3" button_text="Choose Plan" featured="true"]
```

### Contact Information
Contact details with icons:

```markdown
[contact icon="envelope" title="Email" text="contact@example.com" link="mailto:contact@example.com" button_text="Send Email"]
```

### Newsletter Signup
Newsletter subscription prompts:

```markdown
[newsletter title="Stay Updated" subtitle="Get our latest news" button_text="Subscribe" modal_target="newsletterModal"]
```

### Image Gallery
Photo galleries with modal previews:

```markdown
[gallery image="photo-url" title="Photo Title" width="3"]
```

### Modal Dialogs
Interactive forms and dialogs:

```markdown
[modal id="contactModal" title="Contact Us" form_type="contact" subtitle="Get in touch" include_phone="true" button_text="Send"]
```

**Form Types:**
- `email` - Email signup forms
- `newsletter` - Newsletter subscription
- `contact` - Full contact forms with message

**Form Options:**
- `include_name="true"` - Add name field
- `include_phone="true"` - Add phone field
- `include_company="true"` - Add company field

## Layout Tips

### Bootstrap Grid System
Wrap components in Bootstrap grid for proper layout:

```markdown
<div class="container">
<div class="row">

[card title="Card 1" width="4"]
[card title="Card 2" width="4"]
[card title="Card 3" width="4"]

</div>
</div>
```

### Responsive Design
All components are mobile-responsive by default. Use width parameters to control desktop layout.

## Form Management

All form submissions are automatically saved to the database and can be viewed in the CMS admin panel at `/cms/forms`.

### Accessing Form Data
- Navigate to `/cms` and log in as admin
- Click "Form Submissions" to view all submitted forms
- Filter by form type (email, contact, newsletter)
- Export data or delete old submissions

## Examples in Action

Check out these example pages:
- [Landing Page Example](/landing-example) - Complete landing page with all components
- [Blog Example](/blog-example) - Blog post enhanced with components

## Best Practices

1. **Keep it Simple** - Don't overuse components, they should enhance content
2. **Test Responsiveness** - Always check how components look on mobile devices
3. **Use Consistent Colors** - Stick to your brand's color scheme
4. **Optimize Images** - Use appropriate image sizes for faster loading
5. **Test Forms** - Make sure all modal forms work properly before publishing

## Troubleshooting

**Component not rendering?**
- Check bracket syntax `[component param="value"]`
- Ensure all quotes are properly closed
- Check parameter spelling

**Modal not working?**
- Verify modal ID matches the `modal_target` parameter
- Make sure the modal component is included on the page

**Forms not submitting?**
- Check browser console for JavaScript errors
- Verify form fields are properly configured
- Test with simple email form first

Need help? [Contact our support team](/contact) for assistance with components and forms.