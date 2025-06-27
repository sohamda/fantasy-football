# Poly Frontend - Fantasy Football Registration

A modern, responsive React application for user registration and subscription management for the Poly Fantasy Football system.

## Features

- **Multi-step Registration Flow**: Intuitive 3-step process with progress tracking
- **Subscription Plans**: 4 different subscription tiers with comprehensive feature comparison
- **Form Validation**: Real-time validation with user-friendly error messages
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI**: Built with Tailwind CSS and Lucide React icons

## Subscription Plans

### 1. Starter (€9.99/month)
- 1 team generation per week
- Basic player stats
- Standard 4-3-3 formation
- Email support

### 2. Professional (€19.99/month) - Most Popular
- 3 team generations per week
- Historical player statistics
- Formation flexibility
- Priority email support
- Weekly strategy insights
- Access to Eredivisie news

### 3. Expert (€34.99/month)
- Unlimited team generations
- Full historical data access
- Manager performance analytics
- Real-time Eredivisie news
- Advanced AI predictions
- Phone support

### 4. Enterprise (€59.99/month)
- Everything in Expert plan
- Multi-league management
- API access
- Custom analytics dashboard
- Dedicated account manager
- 24/7 priority support

## Tech Stack

- **React 18** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **React Router DOM** for navigation
- **Lucide React** for icons
- **ESLint** for code quality

## Getting Started

### Prerequisites
- Node.js 18+ and npm/yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd code/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and visit `http://localhost:3000`

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Checkbox.tsx
│   │   └── Toaster.tsx
│   ├── RegistrationFlow.tsx  # Main registration component
│   └── SubscriptionCard.tsx  # Subscription plan cards
├── data/
│   └── subscriptionPlans.ts  # Plan configurations
├── lib/
│   └── utils.ts         # Utility functions
├── types/
│   └── index.ts         # TypeScript type definitions
├── App.tsx
├── main.tsx
└── index.css
```

## Features in Detail

### Registration Flow
1. **Personal Information**: Name, email, password with validation
2. **Plan Selection**: Interactive cards showing all subscription options
3. **Confirmation**: Review all details before completing registration

### Validation
- Email format validation
- Password strength requirements (8+ chars, uppercase, lowercase, number)
- Form completeness checks
- Terms and conditions acceptance

### UI/UX Features
- Progress indicator showing current step
- Real-time form validation
- Responsive design for all screen sizes
- Accessible components with proper ARIA labels
- Toast notifications for user feedback
- Smooth animations and transitions

## Customization

### Adding New Subscription Plans
Edit `src/data/subscriptionPlans.ts` to add or modify subscription options.

### Styling
The application uses Tailwind CSS. Customize the theme in `tailwind.config.js`.

### Form Fields
Add new form fields by updating the `UserRegistration` type in `src/types/index.ts` and the corresponding form components.

## Contributing

1. Follow the existing code style and patterns
2. Add TypeScript types for new features
3. Include proper error handling
4. Test responsive design on multiple screen sizes
5. Ensure accessibility compliance

## Future Enhancements

- Payment integration
- Email verification
- Social login options
- Plan comparison tool
- User dashboard preview
- Multi-language support
