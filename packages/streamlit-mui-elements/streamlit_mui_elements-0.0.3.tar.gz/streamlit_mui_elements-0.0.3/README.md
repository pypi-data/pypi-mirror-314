# Streamlit Material-UI Form Example

This repository demonstrates how to create beautiful Material-UI components in Streamlit applications, inspired by [streamlit-elements](https://github.com/okld/streamlit-elements) by okld.

## 📝 Description

This project provides a comprehensive implementation of Material-UI components for Streamlit, building upon the integration approach pioneered by streamlit-elements. It includes a wide range of Material-UI elements with full callback support, making it easier to create sophisticated web interfaces within Streamlit applications.

## 🚀 Features

- Comprehensive Material Design components including:
  - Text input fields
  - Selection chips
  - Autocomplete with multiple selection
  - Radio button groups
  - Sliders
  - Checkbox groups
  - Rating component
  - Dropdowns
  - Switches
  - Styled buttons
- Organized layout with cards and dividers
- Full callback support for all components
- State management through session state

## 💡 How It Works

All component callbacks are automatically stored in `st.session_state["events"]`. Individual component states can be accessed using their respective IDs:

## 🎥 Demo
<img src="docs/assets/output.gif" alt="Demo of Material-UI Components" width="500"/>