import React, { useState } from 'react';
import { ArrowLeft, ArrowRight, User, CreditCard, CheckCircle } from 'lucide-react';
import { UserRegistration, RegistrationStep } from '../types';
import { subscriptionPlans } from '../data/subscriptionPlans';
import { validateEmail, validatePassword } from '../lib/utils';
import { Button } from './ui/Button';
import { Input } from './ui/Input';
import { Checkbox } from './ui/Checkbox';
import { SubscriptionCard } from './SubscriptionCard';

const steps: RegistrationStep[] = [
  { id: 1, title: 'Personal Information', description: 'Tell us about yourself', completed: false },
  { id: 2, title: 'Choose Your Plan', description: 'Select the perfect subscription', completed: false },
  { id: 3, title: 'Confirmation', description: 'Review and complete', completed: false },
];

export default function RegistrationFlow() {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<UserRegistration>({
    email: '',
    firstName: '',
    lastName: '',
    password: '',
    confirmPassword: '',
    selectedPlan: '',
    agreeToTerms: false,
    subscribeToNewsletter: false,
  });
  const [errors, setErrors] = useState<Partial<UserRegistration>>({});

  const updateFormData = (field: keyof UserRegistration, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const validateStep = (step: number): boolean => {
    const newErrors: Partial<UserRegistration> = {};

    if (step === 1) {
      if (!formData.firstName.trim()) newErrors.firstName = 'First name is required';
      if (!formData.lastName.trim()) newErrors.lastName = 'Last name is required';
      if (!formData.email.trim()) {
        newErrors.email = 'Email is required';
      } else if (!validateEmail(formData.email)) {
        newErrors.email = 'Please enter a valid email address';
      }
      if (!formData.password) {
        newErrors.password = 'Password is required';
      } else {
        const passwordValidation = validatePassword(formData.password);
        if (!passwordValidation.isValid) {
          newErrors.password = passwordValidation.errors[0];
        }
      }
      if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = 'Passwords do not match';
      }
      if (!formData.agreeToTerms) {
        newErrors.agreeToTerms = 'You must agree to the terms and conditions' as any;
      }
    }

    if (step === 2) {
      if (!formData.selectedPlan) {
        // This will be handled in the UI
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const nextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, 3));
    }
  };

  const prevStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  const handleSubmit = async () => {
    if (!validateStep(currentStep)) return;
    
    // Here you would normally send the data to your API
    console.log('Registration data:', formData);
    
    // Simulate API call
    setTimeout(() => {
      alert('Registration successful! Welcome to Poly Fantasy Football!');
    }, 1000);
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <div className="h-16 w-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <User className="h-8 w-8 text-primary-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Personal Information</h2>
              <p className="text-gray-600">Let's get to know you better</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Input
                label="First Name"
                placeholder="Enter your first name"
                value={formData.firstName}
                onChange={(e) => updateFormData('firstName', e.target.value)}
                error={errors.firstName}
              />
              <Input
                label="Last Name"
                placeholder="Enter your last name"
                value={formData.lastName}
                onChange={(e) => updateFormData('lastName', e.target.value)}
                error={errors.lastName}
              />
            </div>

            <Input
              label="Email Address"
              type="email"
              placeholder="Enter your email address"
              value={formData.email}
              onChange={(e) => updateFormData('email', e.target.value)}
              error={errors.email}
            />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Input
                label="Password"
                type="password"
                placeholder="Create a password"
                value={formData.password}
                onChange={(e) => updateFormData('password', e.target.value)}
                error={errors.password}
              />
              <Input
                label="Confirm Password"
                type="password"
                placeholder="Confirm your password"
                value={formData.confirmPassword}
                onChange={(e) => updateFormData('confirmPassword', e.target.value)}
                error={errors.confirmPassword}
              />
            </div>

            <div className="space-y-4">
              <Checkbox
                label="I agree to the Terms of Service and Privacy Policy"
                checked={formData.agreeToTerms}
                onChange={(e) => updateFormData('agreeToTerms', e.target.checked)}
              />
              {errors.agreeToTerms && (
                <p className="text-sm text-red-600">{errors.agreeToTerms}</p>
              )}
              <Checkbox
                label="Subscribe to our newsletter for fantasy football tips and updates"
                checked={formData.subscribeToNewsletter}
                onChange={(e) => updateFormData('subscribeToNewsletter', e.target.checked)}
              />
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <div className="h-16 w-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CreditCard className="h-8 w-8 text-primary-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Choose Your Plan</h2>
              <p className="text-gray-600">Select the subscription that best fits your fantasy football needs</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-4 gap-6">
              {subscriptionPlans.map((plan) => (
                <SubscriptionCard
                  key={plan.id}
                  plan={plan}
                  isSelected={formData.selectedPlan === plan.id}
                  onSelect={(planId) => updateFormData('selectedPlan', planId)}
                />
              ))}
            </div>

            {!formData.selectedPlan && (
              <div className="text-center">
                <p className="text-red-600">Please select a subscription plan to continue</p>
              </div>
            )}
          </div>
        );

      case 3:
        const selectedPlan = subscriptionPlans.find(plan => plan.id === formData.selectedPlan);
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <div className="h-16 w-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="h-8 w-8 text-green-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Confirm Registration</h2>
              <p className="text-gray-600">Review your information before completing</p>
            </div>

            <div className="bg-white rounded-lg border border-gray-200 p-6 space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Personal Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <span className="text-sm text-gray-600">Name</span>
                    <p className="font-medium">{formData.firstName} {formData.lastName}</p>
                  </div>
                  <div>
                    <span className="text-sm text-gray-600">Email</span>
                    <p className="font-medium">{formData.email}</p>
                  </div>
                </div>
              </div>

              {selectedPlan && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Selected Plan</h3>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="flex justify-between items-center">
                      <div>
                        <h4 className="font-semibold text-gray-900">{selectedPlan.name}</h4>
                        <p className="text-gray-600">{selectedPlan.description}</p>
                      </div>
                      <div className="text-right">
                        <span className="text-2xl font-bold text-gray-900">€{selectedPlan.price}</span>
                        <span className="text-gray-600">/month</span>
                      </div>
                    </div>
                    <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Weekly Generations</span>
                        <p className="font-medium">
                          {selectedPlan.teamGenerations.weekly === -1 ? 'Unlimited' : selectedPlan.teamGenerations.weekly}
                        </p>
                      </div>
                      <div>
                        <span className="text-gray-600">Historical Stats</span>
                        <p className="font-medium">{selectedPlan.historicalStats ? 'Included' : 'Not included'}</p>
                      </div>
                      <div>
                        <span className="text-gray-600">Manager Insights</span>
                        <p className="font-medium">{selectedPlan.managerInsights ? 'Included' : 'Not included'}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Welcome to <span className="text-primary-600">Poly</span>
          </h1>
          <p className="text-xl text-gray-600">AI-Powered Eredivisie Fantasy Football</p>
        </div>

        {/* Progress Steps */}
        <div className="flex justify-center mb-12">
          <div className="flex items-center space-x-8">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center">
                <div className={`flex items-center space-x-3 ${currentStep === step.id ? 'text-primary-600' : currentStep > step.id ? 'text-green-600' : 'text-gray-400'}`}>
                  <div className={`h-10 w-10 rounded-full flex items-center justify-center border-2 ${
                    currentStep === step.id 
                      ? 'border-primary-600 bg-primary-50' 
                      : currentStep > step.id 
                        ? 'border-green-600 bg-green-50' 
                        : 'border-gray-300 bg-white'
                  }`}>
                    {currentStep > step.id ? (
                      <CheckCircle className="h-5 w-5" />
                    ) : (
                      <span className="font-semibold">{step.id}</span>
                    )}
                  </div>
                  <div className="hidden sm:block">
                    <p className="font-medium">{step.title}</p>
                    <p className="text-sm">{step.description}</p>
                  </div>
                </div>
                {index < steps.length - 1 && (
                  <ArrowRight className="h-5 w-5 text-gray-400 ml-8" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Form Content */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          {renderStepContent()}
        </div>

        {/* Navigation Buttons */}
        <div className="flex justify-between">
          <Button
            variant="outline"
            onClick={prevStep}
            disabled={currentStep === 1}
            className="flex items-center space-x-2"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Previous</span>
          </Button>

          {currentStep < 3 ? (
            <Button
              onClick={nextStep}
              disabled={currentStep === 2 && !formData.selectedPlan}
              className="flex items-center space-x-2"
            >
              <span>Next</span>
              <ArrowRight className="h-4 w-4" />
            </Button>
          ) : (
            <Button
              onClick={handleSubmit}
              className="flex items-center space-x-2 bg-green-600 hover:bg-green-700"
            >
              <CheckCircle className="h-4 w-4" />
              <span>Complete Registration</span>
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
