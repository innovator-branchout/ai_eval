# AI Evaluation System - Svelte Frontend Design Specification

## Design Tokens

### Color Palette (Based on README.md)
- **Charcoal**: #394f56 (Primary text, headings, borders)
- **Seagrass**: #4c9482 (Pass labels, accents, successful states)
- **Wine**: #6f1d1b (Fail labels, primary buttons, critical states)
- **Platinum**: #ebeaeb (Backgrounds, surfaces, neutral elements)
- **Fern**: #7ca08a (Neutral labels, secondary elements)

### Typography Scale
- **Heading 1**: 2.5rem (bold) - Main page title
- **Heading 2**: 1.5rem (semi-bold) - Section headers
- **Heading 3**: 1.25rem (medium) - Subsection headers
- **Body Text**: 1rem (regular) - General content
- **Label Text**: 0.9rem (medium) - Status labels and metadata

### Spacing Scale
- **XS**: 0.5rem (8px)
- **S**: 1rem (16px) 
- **M**: 1.5rem (24px)
- **L**: 2rem (32px)
- **XL**: 3rem (48px)

## Layout Strategy

### Page Structure
1. **Header Section**
   - Page title "AI Response Grader"
   - Clear visual hierarchy with seagrass accent color

2. **Input Form Section**
   - Two text areas:
     - Prompt (required) - larger textarea for comprehensive input
     - Response (optional) - smaller textarea with placeholder
   - Model type dropdown with three options: Auto, Prompt Only, Response Only
   - Grade button with premium styling

3. **Results Display Section** 
   - Label display with color coding (green for pass, red for fail)
   - Explanation of the label
   - Semi-circle confidence visualization

4. **History Tracking Section**
   - Recent predictions list with labels and confidence scores

## Interactive Elements

### Grade Button
- **Primary Action**: Large, prominent button with wine background (#6f1d1b)
- **Hover Effect**: Slight darkening of background color
- **Active State**: Subtle shadow effect
- **Disabled State**: Semi-transparent with no hover effect
- **Text**: "Grade" in white, bold font

### Input Fields
- **Text Areas**: 
  - 4-row height for adequate space
  - Charcoal border (#394f56)
  - Rounded corners (4px)
  - Responsive sizing

### Model Type Dropdown
- Clean, minimal styling
- Smooth dropdown animation
- Clear visual distinction from text areas

## Custom Component Blueprint: Semi-Circle Confidence Gauge

### SVG Implementation
- **Shape**: Semi-circle with 180-degree arc
- **Size**: 200px diameter (100px radius)
- **Stroke Width**: 12px
- **Fill Color**: Seagrass (#4c9482) for the filled portion
- **Background**: Light gray (#e0e0e0) for the unfilled portion
- **Value Display**: Centered percentage number (bold, charcoal text)
- **Animation**: Smooth transition when confidence changes

### Data Binding Logic
- Calculate fill percentage: `percentage = confidence * 180` degrees
- Use `stroke-dasharray` and `stroke-dashoffset` for dynamic SVG rendering
- Dynamic rotation based on confidence score (0-180 degrees)

## UX States

### Loading State
- **Visual**: Spinner animation with seagrass color
- **Text**: "Grading..." 
- **Button**: Disabled, no hover effect
- **User Feedback**: Clear indication that operation is in progress

### Success State
- **Visual**: Full results display with:
  - Color-coded label (green for pass, red for fail)
  - Explanation text
  - Confidence semi-circle gauge
- **History**: New entry added to recent predictions list

### Error Handling
- **Network Errors**: 
  - Red error message box
  - Clear description of what went wrong
  - Suggestion to check connection
- **API Errors**:
  - Specific error messages from backend
  - Option to retry the operation
- **Validation Errors**:
  - Prompt field required validation
  - Visual highlighting of invalid fields

### Empty State
- **Initial View**: Clean form with placeholder text
- **No History**: "No previous grades" message with icon
- **No Results**: Clear indication that no grading has been performed yet

## Responsive Design Considerations

### Mobile Layout (max-width: 768px)
- Stacked form elements vertically
- Reduced spacing between elements
- Larger touch targets for buttons and inputs
- Adjusted font sizes for readability

### Tablet Layout (769px - 1024px)
- Two-column layout for input fields
- Optimized spacing for medium screens
- Maintained visual hierarchy

### Desktop Layout (min-width: 1025px)
- Full-width layout with optimal spacing
- Enhanced visual elements
- Consistent typography scaling

## API Integration Points

### Endpoints to Use:
1. `POST /api/predict` - For grading prompt/response pairs
2. `GET /api/health` - For system status verification (optional but useful)
3. `GET /api/categories` - For model information (if needed)

### Data Flow:
1. User fills form and clicks Grade
2. Form data sent to backend API
3. API returns label, confidence score, and explanation
4. Results displayed with appropriate styling
5. History updated with new prediction

## Accessibility Considerations

- Proper semantic HTML structure
- Sufficient color contrast (WCAG 2.1 AA compliant)
- Focus states for interactive elements
- ARIA labels where needed
- Responsive touch targets