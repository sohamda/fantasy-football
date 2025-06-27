export interface SubscriptionPlan {
  id: string;
  name: string;
  price: number;
  description: string;
  features: string[];
  teamGenerations: {
    weekly: number;
    monthly: number;
  };
  historicalStats: boolean;
  managerInsights: boolean;
  newsAccess: boolean;
  priority: 'basic' | 'standard' | 'premium' | 'pro';
  color: string;
  popular?: boolean;
}

export interface UserRegistration {
  email: string;
  firstName: string;
  lastName: string;
  password: string;
  confirmPassword: string;
  selectedPlan: string;
  agreeToTerms: boolean;
  subscribeToNewsletter: boolean;
}

export interface RegistrationStep {
  id: number;
  title: string;
  description: string;
  completed: boolean;
}
