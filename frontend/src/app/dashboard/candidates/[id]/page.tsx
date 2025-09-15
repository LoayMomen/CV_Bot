'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Mail, Phone, Star, TrendingUp, FileText, Brain, Target, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { candidatesAPI } from '@/lib/api';

interface Candidate {
  id: number;
  name: string;
  email: string;
  phone?: string;
  job_id: number;
  total_score: number;
  score_breakdown: {
    semantic_similarity: number;
    keyword_overlap: number;
    experience_match: number;
    education_match: number;
  };
  match_explanation: string;
  structured_data: {
    skills: string[];
    experience_years: number;
    education: string[];
    certifications: string[];
    previous_roles: string[];
    summary?: string;
  };
  status: string;
  created_at: string;
  resume_filename: string;
}

export default function CandidateDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const candidateId = parseInt(params.id as string);

  const [candidate, setCandidate] = useState<Candidate | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (candidateId) {
      fetchCandidate();
    }
  }, [candidateId]);

  const fetchCandidate = async () => {
    try {
      const response = await candidatesAPI.getCandidate(candidateId);
      setCandidate(response.data);
    } catch (err: any) {
      setError('Failed to fetch candidate data');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const updateStatus = async (newStatus: string) => {
    if (!candidate) return;

    setIsUpdating(true);
    try {
      await candidatesAPI.updateCandidateStatus(candidateId, newStatus);
      setCandidate({ ...candidate, status: newStatus });
    } catch (err: any) {
      console.error('Failed to update status:', err);
    } finally {
      setIsUpdating(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'shortlisted': return 'bg-green-100 text-green-800';
      case 'reviewed': return 'bg-blue-100 text-blue-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-lg">Loading candidate details...</div>
      </div>
    );
  }

  if (error || !candidate) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md w-full">
          <CardContent className="text-center py-8">
            <p className="text-red-600 mb-4">{error || 'Candidate not found'}</p>
            <Button asChild>
              <Link href="/dashboard">Back to Dashboard</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center gap-4 mb-8">
          <Button variant="ghost" size="sm" asChild>
            <Link href={`/dashboard/jobs/${candidate.job_id}`}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Job
            </Link>
          </Button>
        </div>

        {/* Candidate Header */}
        <div className="mb-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{candidate.name}</h1>
              <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
                <div className="flex items-center gap-1">
                  <Mail className="w-4 h-4" />
                  {candidate.email}
                </div>
                {candidate.phone && (
                  <div className="flex items-center gap-1">
                    <Phone className="w-4 h-4" />
                    {candidate.phone}
                  </div>
                )}
                <span>Applied {new Date(candidate.created_at).toLocaleDateString()}</span>
              </div>
              <div className="flex items-center gap-4">
                <div className={`text-2xl font-bold ${getScoreColor(candidate.total_score)}`}>
                  {Math.round(candidate.total_score * 100)}% Match
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(candidate.status)}`}>
                  {candidate.status}
                </span>
              </div>
            </div>

            {/* Status Actions */}
            <div className="flex gap-2">
              <Button
                size="sm"
                variant={candidate.status === 'shortlisted' ? 'default' : 'outline'}
                onClick={() => updateStatus('shortlisted')}
                disabled={isUpdating}
              >
                Shortlist
              </Button>
              <Button
                size="sm"
                variant={candidate.status === 'reviewed' ? 'default' : 'outline'}
                onClick={() => updateStatus('reviewed')}
                disabled={isUpdating}
              >
                Mark Reviewed
              </Button>
              <Button
                size="sm"
                variant={candidate.status === 'rejected' ? 'destructive' : 'outline'}
                onClick={() => updateStatus('rejected')}
                disabled={isUpdating}
              >
                Reject
              </Button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column */}
          <div className="space-y-6">
            {/* Score Breakdown */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-blue-500" />
                  Score Breakdown
                </CardTitle>
                <CardDescription>
                  AI-powered matching analysis
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {candidate.score_breakdown && Object.entries(candidate.score_breakdown).map(([key, value]) => {
                  if (key === 'total_weighted_score') return null;
                  const percentage = Math.round((value as number) * 100);
                  const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

                  return (
                    <div key={key}>
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-sm font-medium text-gray-700">{label}</span>
                        <span className={`text-sm font-semibold ${getScoreColor(value as number)}`}>
                          {percentage}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            (value as number) >= 0.8 ? 'bg-green-500' :
                            (value as number) >= 0.6 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </CardContent>
            </Card>

            {/* AI Explanation */}
            {candidate.match_explanation && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Brain className="w-5 h-5 text-purple-500" />
                    AI Match Explanation
                  </CardTitle>
                  <CardDescription>
                    Why this candidate matches the job requirements
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                    {candidate.match_explanation}
                  </p>
                </CardContent>
              </Card>
            )}

            {/* Summary */}
            {candidate.structured_data?.summary && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <User className="w-5 h-5 text-gray-500" />
                    Professional Summary
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 leading-relaxed">
                    {candidate.structured_data.summary}
                  </p>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Skills */}
            {candidate.structured_data?.skills?.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="w-5 h-5 text-blue-500" />
                    Skills
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {candidate.structured_data.skills.map((skill, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Experience & Education */}
            <div className="grid gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Experience</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-gray-900">Years of Experience:</span>
                      <span className="text-lg font-semibold text-blue-600">
                        {candidate.structured_data?.experience_years || 0} years
                      </span>
                    </div>

                    {candidate.structured_data?.previous_roles?.length > 0 && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Previous Roles:</h4>
                        <div className="space-y-1">
                          {candidate.structured_data.previous_roles.map((role, index) => (
                            <div key={index} className="text-sm text-gray-700 capitalize">
                              • {role}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              {candidate.structured_data?.education?.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Education</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {candidate.structured_data.education.map((edu, index) => (
                        <div key={index} className="text-sm text-gray-700">
                          {edu}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Certifications */}
            {candidate.structured_data?.certifications?.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Star className="w-5 h-5 text-yellow-500" />
                    Certifications
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {candidate.structured_data.certifications.map((cert, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <Star className="w-4 h-4 text-yellow-500" />
                        <span className="text-sm text-gray-700">{cert}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Resume File */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="w-5 h-5 text-gray-500" />
                  Resume File
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <FileText className="w-8 h-8 text-gray-400" />
                    <div>
                      <p className="font-medium text-gray-900">{candidate.resume_filename}</p>
                      <p className="text-sm text-gray-600">Uploaded resume</p>
                    </div>
                  </div>
                  <Button size="sm" variant="outline">
                    Download
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}