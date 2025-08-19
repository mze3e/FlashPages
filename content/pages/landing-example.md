---
title: "Landing Page Example"
slug: "landing-example"
layout: "landing"
description: "A comprehensive example showing all available components with shorthand notation"
nav_order: 10
---

# Landing Page Components Demo

This page demonstrates all available components using shorthand notation.

[hero title="Welcome to Our Amazing Product" subtitle="Build beautiful landing pages with simple markdown components" bg_image="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=1200&h=600&fit=crop" button_text="Get Started" modal_target="signupModal" button_color="primary"]

## Features Section

<div class="container">
<div class="row">

[feature icon="rocket" title="Fast & Reliable" text="Lightning-fast performance with 99.9% uptime guarantee" width="4"]

[feature icon="shield-alt" title="Secure by Design" text="Enterprise-grade security with end-to-end encryption" width="4" icon_color="success"]

[feature icon="chart-bar" title="Analytics Included" text="Comprehensive analytics dashboard to track your success" width="4" icon_color="info"]

</div>
</div>

## Customer Testimonials

<div class="container">
<div class="row">

[testimonial author="Sarah Johnson" company="Tech Startup" quote="This product completely transformed how we work. Highly recommended!" image="https://images.unsplash.com/photo-1494790108755-2616b612b5bb?w=150&h=150&fit=crop&crop=face" width="6"]

[testimonial author="Mike Chen" company="Design Agency" quote="The best tool we've ever used. Our productivity increased by 200%!" image="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face" width="6"]

</div>
</div>

## Pricing Plans

<div class="container">
<div class="row">

[pricing title="Starter" price="29" period="month" features="5 Projects,10GB Storage,Email Support,Basic Analytics" button_text="Start Free Trial" modal_target="signupModal" button_color="outline-primary" width="4"]

[pricing title="Professional" price="79" period="month" features="Unlimited Projects,100GB Storage,Priority Support,Advanced Analytics,Custom Integrations" button_text="Choose Professional" modal_target="signupModal" button_color="primary" featured="true" width="4"]

[pricing title="Enterprise" price="199" period="month" features="Everything in Pro,Unlimited Storage,24/7 Phone Support,Custom Development,SLA Guarantee" button_text="Contact Sales" modal_target="contactModal" button_color="outline-primary" width="4"]

</div>
</div>

[cta title="Ready to Get Started?" subtitle="Join thousands of satisfied customers and transform your workflow today" button_text="Start Your Free Trial" modal_target="signupModal" bg_color="primary"]

## Photo Gallery

<div class="container">
<div class="row">

[gallery image="https://images.unsplash.com/photo-1551434678-e076c223a692?w=400&h=300&fit=crop" title="Modern Office" width="3"]

[gallery image="https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=400&h=300&fit=crop" title="Team Meeting" width="3"]

[gallery image="https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=400&h=300&fit=crop" title="Creative Workspace" width="3"]

[gallery image="https://images.unsplash.com/photo-1553877522-43269d4ea984?w=400&h=300&fit=crop" title="Innovation Hub" width="3"]

</div>
</div>

[newsletter title="Stay Updated" subtitle="Get the latest news and updates delivered to your inbox" button_text="Subscribe" modal_target="newsletterModal"]

## Contact Information

<div class="container">
<div class="row">

[contact icon="envelope" title="Email Us" text="support@example.com" link="mailto:support@example.com" button_text="Send Email" width="4"]

[contact icon="phone" title="Call Us" text="+1 (555) 123-4567" link="tel:+15551234567" button_text="Call Now" width="4"]

[contact icon="map-marker-alt" title="Visit Us" text="123 Business St, City, ST 12345" link="https://maps.google.com" button_text="Get Directions" width="4"]

</div>
</div>

<!-- Modal Dialogs -->
[modal id="signupModal" title="Start Your Free Trial" form_type="email" subtitle="Sign up now to get started with your free 14-day trial" include_name="true" button_text="Start Trial"]

[modal id="contactModal" title="Contact Our Sales Team" form_type="contact" subtitle="Let us help you find the perfect plan for your needs" include_phone="true" include_company="true" button_text="Send Message"]

[modal id="newsletterModal" title="Subscribe to Newsletter" form_type="newsletter" subtitle="Stay updated with our latest features and news" button_text="Subscribe"]