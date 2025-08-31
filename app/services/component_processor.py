"""Component processor for handling shorthand markdown notation"""
import re
import json
from typing import Dict, List, Any
from jinja2 import Template
import yaml
from pathlib import Path

class ComponentProcessor:
    """Process component shorthand notation in markdown content"""
    
    def __init__(self):
        self.component_pattern = re.compile(r'\[([a-zA-Z_]+)\s*(.*?)\]', re.MULTILINE | re.DOTALL)
        
    def process_content(self, content: str) -> str:
        """Process all components in the content"""
        def replace_component(match):
            component_type = match.group(1).lower()
            params_str = match.group(2).strip()
            params = self._parse_params(params_str)
            
            return self._render_component(component_type, params)
        
        return self.component_pattern.sub(replace_component, content)
    
    def _parse_params(self, params_str: str) -> Dict[str, Any]:
        """Parse component parameters from string"""
        params = {}
        if not params_str:
            return params
            
        # Parse key="value" or key=value pairs
        param_pattern = re.compile(r'(\w+)=(?:"([^"]*?)"|([^\s]*?)(?:\s|$))')
        
        for match in param_pattern.finditer(params_str):
            key = match.group(1)
            value = match.group(2) or match.group(3)
            params[key] = value.strip()
            
        return params
    
    def _render_component(self, component_type: str, params: Dict[str, Any]) -> str:
        """Render a component based on its type and parameters"""
        try:
            if component_type == 'hero':
                return self._render_hero(params)
            elif component_type == 'card':
                return self._render_card(params)
            elif component_type == 'cta':
                return self._render_cta(params)
            elif component_type == 'feature':
                return self._render_feature(params)
            elif component_type == 'testimonial':
                return self._render_testimonial(params)
            elif component_type == 'pricing':
                return self._render_pricing(params)
            elif component_type == 'gallery':
                return self._render_gallery(params)
            elif component_type == 'contact':
                return self._render_contact(params)
            elif component_type == 'newsletter':
                return self._render_newsletter(params)
            elif component_type == 'modal':
                return self._render_modal(params)
            elif component_type == 'data_editor':
                return self._render_data_editor(params)
            else:
                return f'<!-- Unknown component: {component_type} -->'
        except Exception as e:
            return f'<!-- Error rendering {component_type}: {str(e)} -->'
    
    def _render_data_editor(self, params: Dict[str, Any]) -> str:
        """Render a data editor component"""
        source = params.get('source')
        if not source:
            return '<!-- Data source not specified for data_editor component -->'

        data_dir = Path('content/data')
        data_file = data_dir / f'{source}.yml'

        if not data_file.exists():
            return f'<!-- Data file not found: {data_file} -->'

        with open(data_file, 'r') as f:
            data = yaml.safe_load(f)

        if not data:
            return '<!-- No data to display -->'

        headers = list(data[0].keys())

        template_str = """
<div class="data-editor-wrapper" data-source="{{ source }}">
    <table id="data-editor-{{ source }}" class="table table-bordered">
        <thead>
            <tr>
                {% for header in headers %}
                <th>{{ header }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in data %}
            <tr>
                {% for header in headers %}
                <td contenteditable="true" data-field="{{ header }}">{{ row[header] }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <button class="btn btn-primary mt-2" onclick="saveData('{{ source }}')">Save</button>
</div>
"""
        template = Template(template_str)
        return template.render(source=source, headers=headers, data=data)

    def _render_hero(self, params: Dict[str, Any]) -> str:
        """Render hero section"""
        template = Template("""
<div class="hero-section py-5 mb-5" style="background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{{ bg_image }}') center/cover;">
    <div class="container">
        <div class="row justify-content-center text-center text-white">
            <div class="col-lg-8">
                <h1 class="display-4 fw-bold mb-4">{{ title }}</h1>
                {% if subtitle %}
                <p class="lead mb-4">{{ subtitle }}</p>
                {% endif %}
                {% if button_text and button_url %}
                <a href="{{ button_url }}" class="btn btn-{{ button_color or 'primary' }} btn-lg">{{ button_text }}</a>
                {% endif %}
                {% if modal_target %}
                <button type="button" class="btn btn-{{ button_color or 'primary' }} btn-lg" data-bs-toggle="modal" data-bs-target="#{{ modal_target }}">
                    {{ button_text }}
                </button>
                {% endif %}
            </div>
        </div>
    </div>
</div>
""")
        return template.render(**params)
    
    def _render_card(self, params: Dict[str, Any]) -> str:
        """Render card component"""
        template = Template("""
<div class="col-md-{{ width or '4' }} mb-4">
    <div class="card h-100 shadow-sm">
        {% if image %}
        <img src="{{ image }}" class="card-img-top" alt="{{ title }}">
        {% endif %}
        <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ title }}</h5>
            <p class="card-text flex-grow-1">{{ text }}</p>
            {% if button_text and (button_url or modal_target) %}
            <div class="mt-auto">
                {% if button_url %}
                <a href="{{ button_url }}" class="btn btn-{{ button_color or 'primary' }}">{{ button_text }}</a>
                {% elif modal_target %}
                <button type="button" class="btn btn-{{ button_color or 'primary' }}" data-bs-toggle="modal" data-bs-target="#{{ modal_target }}">
                    {{ button_text }}
                </button>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
</div>
""")
        return template.render(**params)
    
    def _render_cta(self, params: Dict[str, Any]) -> str:
        """Render call-to-action section"""
        template = Template("""
<div class="cta-section py-5 my-5 bg-{{ bg_color or 'primary' }} text-white text-center">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <h2 class="mb-3">{{ title }}</h2>
                {% if subtitle %}
                <p class="lead mb-4">{{ subtitle }}</p>
                {% endif %}
                {% if button_text and (button_url or modal_target) %}
                {% if button_url %}
                <a href="{{ button_url }}" class="btn btn-{{ button_color or 'light' }} btn-lg">{{ button_text }}</a>
                {% elif modal_target %}
                <button type="button" class="btn btn-{{ button_color or 'light' }} btn-lg" data-bs-toggle="modal" data-bs-target="#{{ modal_target }}">
                    {{ button_text }}
                </button>
                {% endif %}
                {% endif %}
            </div>
        </div>
    </div>
</div>
""")
        return template.render(**params)
    
    def _render_feature(self, params: Dict[str, Any]) -> str:
        """Render feature section"""
        template = Template("""
<div class="col-md-{{ width or '4' }} mb-4 text-center">
    {% if icon %}
    <div class="feature-icon mb-3">
        <i class="fas fa-{{ icon }} fa-3x text-{{ icon_color or 'primary' }}"></i>
    </div>
    {% endif %}
    <h4>{{ title }}</h4>
    <p>{{ text }}</p>
</div>
""")
        return template.render(**params)
    
    def _render_testimonial(self, params: Dict[str, Any]) -> str:
        """Render testimonial component"""
        template = Template("""
<div class="col-md-{{ width or '6' }} mb-4">
    <div class="testimonial-card p-4 bg-light rounded">
        <blockquote class="blockquote">
            <p class="mb-3">"{{ quote }}"</p>
            <footer class="blockquote-footer">
                {% if image %}
                <img src="{{ image }}" class="rounded-circle me-2" width="40" height="40" alt="{{ author }}">
                {% endif %}
                <strong>{{ author }}</strong>
                {% if company %}
                <span class="text-muted">{{ company }}</span>
                {% endif %}
            </footer>
        </blockquote>
    </div>
</div>
""")
        return template.render(**params)
    
    def _render_pricing(self, params: Dict[str, Any]) -> str:
        """Render pricing card"""
        template = Template("""
<div class="col-md-{{ width or '4' }} mb-4">
    <div class="card pricing-card h-100 text-center{% if featured %} border-primary{% endif %}">
        {% if featured %}
        <div class="card-header bg-primary text-white">
            <h6 class="mb-0">Most Popular</h6>
        </div>
        {% endif %}
        <div class="card-body d-flex flex-column">
            <h4>{{ title }}</h4>
            <div class="price mb-3">
                <span class="h2">${{ price }}</span>
                {% if period %}
                <small class="text-muted">/ {{ period }}</small>
                {% endif %}
            </div>
            <ul class="list-unstyled mb-4 flex-grow-1">
                {% set features = features.split(',') if features else [] %}
                {% for feature in features %}
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>{{ feature.strip() }}</li>
                {% endfor %}
            </ul>
            {% if button_text and (button_url or modal_target) %}
            <div class="mt-auto">
                {% if button_url %}
                <a href="{{ button_url }}" class="btn btn-{{ button_color or 'primary' }} w-100">{{ button_text }}</a>
                {% elif modal_target %}
                <button type="button" class="btn btn-{{ button_color or 'primary' }} w-100" data-bs-toggle="modal" data-bs-target="#{{ modal_target }}">
                    {{ button_text }}
                </button>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
</div>
""")
        return template.render(**params)
    
    def _render_gallery(self, params: Dict[str, Any]) -> str:
        """Render image gallery"""
        template = Template("""
<div class="col-md-{{ width or '3' }} mb-4">
    <div class="gallery-item">
        <img src="{{ image }}" class="img-fluid rounded shadow-sm" alt="{{ title or 'Gallery image' }}" 
             data-bs-toggle="modal" data-bs-target="#galleryModal" data-bs-slide-to="{{ index or '0' }}">
        {% if title %}
        <h6 class="mt-2 text-center">{{ title }}</h6>
        {% endif %}
    </div>
</div>
""")
        return template.render(**params)
    
    def _render_contact(self, params: Dict[str, Any]) -> str:
        """Render contact information"""
        template = Template("""
<div class="col-md-{{ width or '4' }} mb-4 text-center">
    {% if icon %}
    <div class="contact-icon mb-3">
        <i class="fas fa-{{ icon }} fa-2x text-{{ icon_color or 'primary' }}"></i>
    </div>
    {% endif %}
    <h5>{{ title }}</h5>
    {% if text %}
    <p>{{ text }}</p>
    {% endif %}
    {% if link %}
    <a href="{{ link }}" class="btn btn-outline-{{ button_color or 'primary' }}">{{ button_text or 'Contact' }}</a>
    {% endif %}
</div>
""")
        return template.render(**params)
    
    def _render_newsletter(self, params: Dict[str, Any]) -> str:
        """Render newsletter signup"""
        template = Template("""
<div class="newsletter-section p-4 bg-light rounded">
    <div class="row align-items-center">
        <div class="col-md-8">
            <h5>{{ title or 'Subscribe to our Newsletter' }}</h5>
            {% if subtitle %}
            <p class="mb-0">{{ subtitle }}</p>
            {% endif %}
        </div>
        <div class="col-md-4 text-end">
            <button type="button" class="btn btn-{{ button_color or 'primary' }}" data-bs-toggle="modal" data-bs-target="#{{ modal_target or 'newsletterModal' }}">
                {{ button_text or 'Subscribe' }}
            </button>
        </div>
    </div>
</div>
""")
        return template.render(**params)
    
    def _render_modal(self, params: Dict[str, Any]) -> str:
        """Render modal dialog"""
        modal_id = params.get('id', 'defaultModal')
        form_type = params.get('form_type', 'contact')
        
        template = Template("""
<div class="modal fade" id="{{ modal_id }}" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">{{ title or 'Contact Us' }}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                {% if subtitle %}
                <p>{{ subtitle }}</p>
                {% endif %}
                <form id="{{ form_id or (modal_id + 'Form') }}" data-form-type="{{ form_type }}">
                    {% if form_type == 'email' or form_type == 'newsletter' %}
                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" class="form-control" name="email" required>
                    </div>
                    {% if include_name %}
                    <div class="mb-3">
                        <label for="name" class="form-label">Name</label>
                        <input type="text" class="form-control" name="name">
                    </div>
                    {% endif %}
                    {% elif form_type == 'contact' %}
                    <div class="mb-3">
                        <label for="name" class="form-label">Name</label>
                        <input type="text" class="form-control" name="name" required>
                    </div>
                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" class="form-control" name="email" required>
                    </div>
                    {% if include_phone %}
                    <div class="mb-3">
                        <label for="phone" class="form-label">Phone</label>
                        <input type="tel" class="form-control" name="phone">
                    </div>
                    {% endif %}
                    {% if include_company %}
                    <div class="mb-3">
                        <label for="company" class="form-label">Company</label>
                        <input type="text" class="form-control" name="company">
                    </div>
                    {% endif %}
                    <div class="mb-3">
                        <label for="subject" class="form-label">Subject</label>
                        <input type="text" class="form-control" name="subject">
                    </div>
                    <div class="mb-3">
                        <label for="message" class="form-label">Message</label>
                        <textarea class="form-control" name="message" rows="4" required></textarea>
                    </div>
                    {% endif %}
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-{{ button_color or 'primary' }}" onclick="submitForm('{{ form_id or (modal_id + 'Form') }}')">
                    {{ button_text or 'Submit' }}
                </button>
            </div>
        </div>
    </div>
</div>
""")
        return template.render(modal_id=modal_id, form_type=form_type, **params)