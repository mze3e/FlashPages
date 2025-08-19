---
title: "Component System Guide"
slug: "components"
layout: "docs"
description: "Complete guide to using shorthand markdown components for building beautiful Bootstrap layouts"
nav_order: 5
---

# Component System Guide

This guide shows you how to use the shorthand component notation to create beautiful Bootstrap UI elements with simple markdown syntax.

## Basic Syntax

Components use the format: `[component param="value" param2="value"]`

All components are responsive and use Bootstrap 5 classes for consistent styling.

## Available Components

### 1. Hero Sections

Create eye-catching hero sections with background images and call-to-action buttons.

```markdown
[hero title="Your Amazing Title" subtitle="Compelling subtitle text" bg_image="https://example.com/image.jpg" button_text="Get Started" modal_target="signupModal" button_color="primary"]
```

**Parameters:**
- `title` - Main heading text
- `subtitle` - Secondary text below title
- `bg_image` - Background image URL
- `button_text` - CTA button text
- `modal_target` - Modal ID to open
- `button_color` - Bootstrap color (primary, secondary, success, etc.)

### 2. Feature Highlights

Display features with icons in responsive columns.

```markdown
[feature icon="rocket" title="Fast Performance" text="Lightning-fast loading times" width="4" icon_color="primary"]
```

**Parameters:**
- `icon` - Font Awesome icon name (without fa- prefix)
- `title` - Feature title
- `text` - Feature description
- `width` - Bootstrap column width (1-12)
- `icon_color` - Bootstrap color for icon

### 3. Testimonials

Show customer testimonials with photos and company info.

```markdown
[testimonial author="John Smith" company="Tech Corp" quote="This product is amazing!" image="https://example.com/photo.jpg" width="6"]
```

**Parameters:**
- `author` - Customer name
- `company` - Company name
- `quote` - Testimonial text
- `image` - Customer photo URL
- `width` - Bootstrap column width

### 4. Pricing Cards

Create pricing tables with feature lists and CTA buttons.

```markdown
[pricing title="Pro Plan" price="99" period="month" features="Feature 1,Feature 2,Feature 3" button_text="Choose Plan" modal_target="signupModal" button_color="primary" featured="true" width="4"]
```

**Parameters:**
- `title` - Plan name
- `price` - Price amount
- `period` - Billing period (month, year)
- `features` - Comma-separated feature list
- `button_text` - CTA button text
- `modal_target` - Modal to open
- `button_color` - Button color
- `featured` - "true" to highlight as featured plan
- `width` - Column width

### 5. Cards

General-purpose content cards with images and buttons.

```markdown
[card title="Card Title" text="Card description" image="https://example.com/image.jpg" button_text="Learn More" button_link="/page" width="4"]
```

**Parameters:**
- `title` - Card title
- `text` - Card body text
- `image` - Card image URL
- `button_text` - Button text
- `button_link` - Button destination URL
- `width` - Column width

### 6. Call-to-Action Sections

Full-width promotional sections with gradients.

```markdown
[cta title="Ready to Start?" subtitle="Join thousands of happy customers" button_text="Get Started" modal_target="signupModal" bg_color="primary"]
```

**Parameters:**
- `title` - Main CTA heading
- `subtitle` - Supporting text
- `button_text` - Button text
- `modal_target` - Modal to open
- `bg_color` - Background color

### 7. Image Galleries

Responsive image galleries with modal previews.

```markdown
[gallery images="image1.jpg,image2.jpg,image3.jpg" titles="Title 1,Title 2,Title 3"]
```

**Parameters:**
- `images` - Comma-separated image URLs
- `titles` - Comma-separated image titles

### 8. Contact Information

Display contact details with icons.

```markdown
[contact email="hello@company.com" phone="+1-555-0123" address="123 Main St, City" website="https://company.com"]
```

**Parameters:**
- `email` - Contact email
- `phone` - Phone number
- `address` - Physical address
- `website` - Website URL

### 9. Newsletter Signup

Email collection forms with database storage.

```markdown
[newsletter title="Stay Updated" subtitle="Get the latest news and updates" placeholder="Enter your email" button_text="Subscribe"]
```

**Parameters:**
- `title` - Newsletter heading
- `subtitle` - Description text
- `placeholder` - Input placeholder text
- `button_text` - Submit button text

## Layout with Bootstrap Grid

Use Bootstrap's grid system to create responsive layouts:

```markdown
<div class="container">
<div class="row">

[feature icon="star" title="Feature 1" text="Description" width="4"]
[feature icon="heart" title="Feature 2" text="Description" width="4"]  
[feature icon="thumbs-up" title="Feature 3" text="Description" width="4"]

</div>
</div>
```

## Modal Integration

Many components support modal integration for forms:

1. **Email Signup Modal** (`signupModal`)
2. **Contact Form Modal** (`contactModal`)
3. **Newsletter Modal** (`newsletterModal`)

These modals automatically collect form data and store it in the database.

## Examples

### Landing Page Section
```markdown
[hero title="Transform Your Business" subtitle="Powerful tools for modern teams" bg_image="hero-bg.jpg" button_text="Start Free Trial" modal_target="signupModal" button_color="primary"]

<div class="container my-5">
<div class="row">

[feature icon="rocket" title="Fast" text="Lightning performance" width="4"]
[feature icon="shield" title="Secure" text="Enterprise security" width="4"]
[feature icon="chart-line" title="Analytics" text="Detailed insights" width="4"]

</div>
</div>

[cta title="Ready to Get Started?" subtitle="Join over 10,000 satisfied customers" button_text="Start Your Trial" modal_target="signupModal" bg_color="success"]
```

### Pricing Section
```markdown
<div class="container">
<div class="row justify-content-center">

[pricing title="Starter" price="29" period="month" features="5 Projects,10GB Storage,Email Support" button_text="Choose Starter" modal_target="signupModal" width="4"]

[pricing title="Pro" price="79" period="month" features="Unlimited Projects,100GB Storage,Priority Support,Advanced Features" button_text="Choose Pro" modal_target="signupModal" button_color="primary" featured="true" width="4"]

[pricing title="Enterprise" price="199" period="month" features="Everything in Pro,Custom Integration,24/7 Support,SLA" button_text="Contact Sales" modal_target="contactModal" width="4"]

</div>
</div>
```

## Form Data Management

All form submissions are automatically stored in the database. Administrators can view and manage submissions at `/cms/forms`.

The system captures:
- Email addresses
- Contact form messages
- Newsletter subscriptions
- Timestamps and form types

## Best Practices

1. **Use containers** - Wrap components in Bootstrap containers for proper spacing
2. **Consider mobile** - Test on different screen sizes
3. **Optimize images** - Use appropriately sized images for better performance  
4. **Consistent colors** - Stick to your site's color scheme
5. **Clear CTAs** - Use action-oriented button text
6. **Test modals** - Verify forms work correctly before publishing

## Custom Styling

Components inherit your site's Bootstrap theme and can be further customized with CSS classes and the custom.css file.