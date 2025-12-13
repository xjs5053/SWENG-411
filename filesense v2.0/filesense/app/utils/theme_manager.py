"""
Theme Manager - Handle application themes and colors
"""
import customtkinter as ctk
from typing import Dict, Optional
from app.models import Settings, get_session


class ThemeManager:
    """Manage application themes and colors"""
    
    # Theme definitions
    THEMES = {
        'light': {
            'name': 'Light',
            'appearance': 'light',
            'primary': '#2E86AB',
            'primary_hover': '#1a5270',
            'accent': '#FFD93D',
            'accent_hover': '#e6c236',
            'success': '#6A994E',
            'success_hover': '#5a8440',
            'danger': '#EF4444',
            'danger_hover': '#dc2626',
            'warning': '#FF9800',
            'background': '#f5f5f5',
            'surface': '#ffffff',
            'surface_secondary': '#f9f9f9',
            'text_primary': '#333333',
            'text_secondary': '#666666',
            'text_muted': '#999999',
            'border': '#e0e0e0',
            'sidebar_bg': '#2E86AB',
            'sidebar_text': '#ffffff',
            'sidebar_active_bg': '#FFD93D',
            'sidebar_active_text': '#2E86AB',
        },
        'dark': {
            'name': 'Dark',
            'appearance': 'dark',
            'primary': '#3B9BC9',
            'primary_hover': '#2E86AB',
            'accent': '#FFD93D',
            'accent_hover': '#e6c236',
            'success': '#7CB45D',
            'success_hover': '#6A994E',
            'danger': '#F87171',
            'danger_hover': '#EF4444',
            'warning': '#FFB74D',
            'background': '#1a1a1a',
            'surface': '#2d2d2d',
            'surface_secondary': '#3d3d3d',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'text_muted': '#808080',
            'border': '#404040',
            'sidebar_bg': '#1f3a4d',
            'sidebar_text': '#ffffff',
            'sidebar_active_bg': '#FFD93D',
            'sidebar_active_text': '#1f3a4d',
        },
        'blue': {
            'name': 'Ocean Blue',
            'appearance': 'light',
            'primary': '#1976D2',
            'primary_hover': '#1565C0',
            'accent': '#00BCD4',
            'accent_hover': '#00ACC1',
            'success': '#4CAF50',
            'success_hover': '#43A047',
            'danger': '#F44336',
            'danger_hover': '#E53935',
            'warning': '#FF9800',
            'background': '#E3F2FD',
            'surface': '#ffffff',
            'surface_secondary': '#BBDEFB',
            'text_primary': '#0D47A1',
            'text_secondary': '#1976D2',
            'text_muted': '#64B5F6',
            'border': '#90CAF9',
            'sidebar_bg': '#0D47A1',
            'sidebar_text': '#ffffff',
            'sidebar_active_bg': '#00BCD4',
            'sidebar_active_text': '#ffffff',
        },
        'green': {
            'name': 'Forest Green',
            'appearance': 'light',
            'primary': '#2E7D32',
            'primary_hover': '#1B5E20',
            'accent': '#8BC34A',
            'accent_hover': '#7CB342',
            'success': '#4CAF50',
            'success_hover': '#43A047',
            'danger': '#D32F2F',
            'danger_hover': '#C62828',
            'warning': '#FFA000',
            'background': '#E8F5E9',
            'surface': '#ffffff',
            'surface_secondary': '#C8E6C9',
            'text_primary': '#1B5E20',
            'text_secondary': '#2E7D32',
            'text_muted': '#66BB6A',
            'border': '#A5D6A7',
            'sidebar_bg': '#1B5E20',
            'sidebar_text': '#ffffff',
            'sidebar_active_bg': '#8BC34A',
            'sidebar_active_text': '#1B5E20',
        },
    }
    
    _current_theme = 'light'
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Load saved theme preference
        self.load_theme_preference()
    
    def load_theme_preference(self):
        """Load theme preference from database"""
        try:
            session = get_session()
            setting = session.query(Settings).filter_by(key='theme').first()
            if setting and setting.value in self.THEMES:
                self._current_theme = setting.value
        except Exception as e:
            print(f"Error loading theme preference: {e}")
    
    def save_theme_preference(self):
        """Save theme preference to database"""
        try:
            session = get_session()
            setting = session.query(Settings).filter_by(key='theme').first()
            
            if setting:
                setting.value = self._current_theme
            else:
                setting = Settings(key='theme', value=self._current_theme)
                session.add(setting)
            
            session.commit()
        except Exception as e:
            print(f"Error saving theme preference: {e}")
    
    @property
    def current_theme(self) -> str:
        """Get current theme name"""
        return self._current_theme
    
    @property
    def colors(self) -> Dict[str, str]:
        """Get current theme colors"""
        return self.THEMES.get(self._current_theme, self.THEMES['light'])
    
    def set_theme(self, theme_name: str) -> bool:
        """Set current theme"""
        if theme_name not in self.THEMES:
            return False
        
        self._current_theme = theme_name
        theme = self.THEMES[theme_name]
        
        # Set CustomTkinter appearance mode
        ctk.set_appearance_mode(theme['appearance'])
        
        # Save preference
        self.save_theme_preference()
        
        return True
    
    def get_available_themes(self) -> Dict[str, str]:
        """Get list of available themes"""
        return {key: theme['name'] for key, theme in self.THEMES.items()}
    
    def get_color(self, color_name: str) -> str:
        """Get specific color from current theme"""
        return self.colors.get(color_name, '#000000')
    
    def apply_to_widget(self, widget, widget_type: str = 'default'):
        """Apply theme colors to a widget"""
        colors = self.colors
        
        try:
            if widget_type == 'button_primary':
                widget.configure(
                    fg_color=colors['primary'],
                    hover_color=colors['primary_hover'],
                    text_color='white'
                )
            elif widget_type == 'button_secondary':
                widget.configure(
                    fg_color=colors['surface'],
                    hover_color=colors['surface_secondary'],
                    text_color=colors['primary'],
                    border_color=colors['primary'],
                    border_width=2
                )
            elif widget_type == 'button_success':
                widget.configure(
                    fg_color=colors['success'],
                    hover_color=colors['success_hover'],
                    text_color='white'
                )
            elif widget_type == 'button_danger':
                widget.configure(
                    fg_color=colors['danger'],
                    hover_color=colors['danger_hover'],
                    text_color='white'
                )
            elif widget_type == 'frame':
                widget.configure(fg_color=colors['surface'])
            elif widget_type == 'frame_secondary':
                widget.configure(fg_color=colors['surface_secondary'])
            elif widget_type == 'label_title':
                widget.configure(text_color=colors['primary'])
            elif widget_type == 'label_secondary':
                widget.configure(text_color=colors['text_secondary'])
            elif widget_type == 'label_muted':
                widget.configure(text_color=colors['text_muted'])
        except Exception as e:
            print(f"Error applying theme to widget: {e}")
    
    @staticmethod
    def get_icon_color(theme_name: str = None) -> str:
        """Get appropriate icon color for theme"""
        if theme_name is None:
            theme_name = ThemeManager._current_theme
        
        theme = ThemeManager.THEMES.get(theme_name, ThemeManager.THEMES['light'])
        return theme['text_primary']


# Convenience function for getting colors
def get_color(color_name: str) -> str:
    """Get color from current theme"""
    return ThemeManager().get_color(color_name)


# Convenience function for getting theme manager instance
def get_theme_manager() -> ThemeManager:
    """Get theme manager instance"""
    return ThemeManager()
