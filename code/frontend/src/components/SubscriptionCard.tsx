import React from 'react';
import { Check, Star } from 'lucide-react';
import { SubscriptionPlan } from '../types';
import { formatPrice } from '../lib/utils';
import { Button } from './ui/Button';

interface SubscriptionCardProps {
  plan: SubscriptionPlan;
  isSelected: boolean;
  onSelect: (planId: string) => void;
}

export const SubscriptionCard: React.FC<SubscriptionCardProps> = ({
  plan,
  isSelected,
  onSelect,
}) => {
  return (
    <div
      className={`relative rounded-xl border-2 p-6 transition-all duration-200 cursor-pointer ${
        isSelected
          ? 'border-primary-500 bg-primary-50 shadow-lg'
          : 'border-gray-200 bg-white hover:border-primary-300 hover:shadow-md'
      }`}
      onClick={() => onSelect(plan.id)}
    >
      {plan.popular && (
        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
          <div className="flex items-center space-x-1 bg-orange-500 text-white px-3 py-1 rounded-full text-sm font-medium">
            <Star className="h-4 w-4" />
            <span>Most Popular</span>
          </div>
        </div>
      )}

      <div className="text-center">
        <div className={`h-12 w-12 mx-auto mb-4 rounded-lg bg-gradient-to-r ${plan.color} flex items-center justify-center`}>
          <span className="text-white font-bold text-xl">
            {plan.name.charAt(0)}
          </span>
        </div>
        
        <h3 className="text-xl font-bold text-gray-900 mb-2">{plan.name}</h3>
        <p className="text-gray-600 mb-4">{plan.description}</p>
        
        <div className="mb-6">
          <span className="text-3xl font-bold text-gray-900">
            {formatPrice(plan.price)}
          </span>
          <span className="text-gray-600">/month</span>
        </div>
      </div>

      <div className="space-y-3 mb-6">
        {plan.features.map((feature, index) => (
          <div key={index} className="flex items-start space-x-3">
            <Check className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
            <span className="text-gray-700 text-sm">{feature}</span>
          </div>
        ))}
      </div>

      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <h4 className="font-semibold text-gray-900 mb-2">Team Generation</h4>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-sm text-gray-600">Weekly</span>
            <p className="font-medium">
              {plan.teamGenerations.weekly === -1 ? 'Unlimited' : `${plan.teamGenerations.weekly} teams`}
            </p>
          </div>
          <div>
            <span className="text-sm text-gray-600">Monthly</span>
            <p className="font-medium">
              {plan.teamGenerations.monthly === -1 ? 'Unlimited' : `${plan.teamGenerations.monthly} teams`}
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-2 mb-6">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Historical Stats</span>
          <span className={`text-sm font-medium ${plan.historicalStats ? 'text-green-600' : 'text-gray-400'}`}>
            {plan.historicalStats ? 'Included' : 'Not included'}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Manager Insights</span>
          <span className={`text-sm font-medium ${plan.managerInsights ? 'text-green-600' : 'text-gray-400'}`}>
            {plan.managerInsights ? 'Included' : 'Not included'}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Eredivisie News</span>
          <span className={`text-sm font-medium ${plan.newsAccess ? 'text-green-600' : 'text-gray-400'}`}>
            {plan.newsAccess ? 'Included' : 'Not included'}
          </span>
        </div>
      </div>

      <Button
        variant={isSelected ? 'primary' : 'outline'}
        className="w-full"
        size="lg"
      >
        {isSelected ? 'Selected Plan' : 'Select Plan'}
      </Button>
    </div>
  );
};
