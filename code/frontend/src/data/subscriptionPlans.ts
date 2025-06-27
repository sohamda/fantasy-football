import { SubscriptionPlan } from '../types';

export const subscriptionPlans: SubscriptionPlan[] = [
  {
    id: 'starter',
    name: 'Starter',
    price: 9.99,
    description: 'Perfect for casual fantasy football fans',
    features: [
      '1 team generation per week',
      'Basic player stats',
      'Standard 4-3-3 formation',
      'Email support'
    ],
    teamGenerations: {
      weekly: 1,
      monthly: 4
    },
    historicalStats: false,
    managerInsights: false,
    newsAccess: false,
    priority: 'basic',
    color: 'from-blue-500 to-blue-600'
  },
  {
    id: 'professional',
    name: 'Professional',
    price: 19.99,
    description: 'For serious fantasy football strategists',
    features: [
      '3 team generations per week',
      'Historical player statistics',
      'Formation flexibility',
      'Priority email support',
      'Weekly strategy insights'
    ],
    teamGenerations: {
      weekly: 3,
      monthly: 12
    },
    historicalStats: true,
    managerInsights: false,
    newsAccess: true,
    priority: 'standard',
    color: 'from-green-500 to-green-600',
    popular: true
  },
  {
    id: 'expert',
    name: 'Expert',
    price: 34.99,
    description: 'Advanced analytics and unlimited generations',
    features: [
      'Unlimited team generations',
      'Full historical data access',
      'Manager performance analytics',
      'Real-time Eredivisie news',
      'Advanced AI predictions',
      'Phone support'
    ],
    teamGenerations: {
      weekly: -1, // unlimited
      monthly: -1
    },
    historicalStats: true,
    managerInsights: true,
    newsAccess: true,
    priority: 'premium',
    color: 'from-purple-500 to-purple-600'
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 59.99,
    description: 'For fantasy football leagues and professionals',
    features: [
      'Everything in Expert',
      'Multi-league management',
      'API access',
      'Custom analytics dashboard',
      'Dedicated account manager',
      '24/7 priority support'
    ],
    teamGenerations: {
      weekly: -1,
      monthly: -1
    },
    historicalStats: true,
    managerInsights: true,
    newsAccess: true,
    priority: 'pro',
    color: 'from-orange-500 to-red-500'
  }
];
