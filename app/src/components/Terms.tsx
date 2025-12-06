import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { BackgroundGraph } from './BackgroundGraph';

export function Terms() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const lastUpdated = 'December 5, 2025';

  return (
    <div className="min-h-screen bg-tana-bg text-tana-text">
      {/* Background Effects */}
      <BackgroundGraph />

      {/* Navigation */}
      <nav
        className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled ? 'bg-tana-bg/80 backdrop-blur-md border-b border-tana-border' : 'bg-transparent'}`}
      >
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <span className="text-white font-bold text-sm">TC</span>
            </div>
            <Link to="/" className="font-bold text-lg tracking-tight">
              TanaChat<span className="text-tana-muted">.ai</span>
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            <Link
              to="/"
              className="text-sm font-medium text-tana-muted hover:text-white transition-colors"
            >
              Home
            </Link>
            <Link
              to="/chat"
              className="text-sm font-medium text-tana-muted hover:text-white transition-colors"
            >
              Chat
            </Link>
            <Link
              to="/privacy"
              className="text-sm font-medium text-tana-muted hover:text-white transition-colors"
            >
              Privacy
            </Link>
            <Link
              to="/signin"
              className="px-4 py-2 rounded-full bg-white text-black text-sm font-semibold hover:bg-gray-200 transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="relative z-10 pt-32 pb-20 px-6">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400">
                Terms of Service
              </span>
            </h1>
            <p className="text-tana-muted text-lg">
              Your agreement with TanaChat.ai for using our AI-powered knowledge platform.
            </p>
            <p className="text-tana-muted text-sm mt-2">Last updated: {lastUpdated}</p>
          </div>

          {/* Content Sections */}
          <div className="space-y-12">
            {/* Agreement to Terms */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">1. Agreement to Terms</h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                Welcome to TanaChat.ai ("TanaChat," "we," "us," or "our"). These Terms of Service
                ("Terms") govern your access to and use of our website, services, and applications
                (the "Service").
              </p>
              <p className="text-tana-muted leading-relaxed">
                By accessing or using our Service, you agree to be bound by these Terms, our Privacy
                Policy, and any additional terms and conditions that may apply to specific features
                of the Service. If you do not agree to these Terms, you may not access or use the
                Service.
              </p>
            </section>

            {/* Description of Service */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">2. Description of Service</h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                TanaChat.ai is an AI-powered platform that integrates with Tana workspaces to
                provide intelligent chat capabilities, knowledge graph analysis, and productivity
                tools. Our Service includes:
              </p>
              <ul className="space-y-2 text-tana-muted list-disc list-inside">
                <li>AI-powered chat interface with Claude and ChatGPT integration</li>
                <li>Tana workspace import and analysis capabilities</li>
                <li>CLI tools for batch processing and automation</li>
                <li>Model Context Protocol (MCP) server for advanced integrations</li>
                <li>API endpoints for third-party developer access</li>
              </ul>
            </section>

            {/* User Accounts */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">3. User Accounts</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">3.1 Registration</h3>
                  <p className="text-tana-muted leading-relaxed">
                    To access certain features of the Service, you must create an account. You agree
                    to provide accurate, current, and complete information during registration and
                    to update such information to keep it accurate, current, and complete.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">3.2 Account Security</h3>
                  <p className="text-tana-muted leading-relaxed">
                    You are responsible for safeguarding your account credentials and for all
                    activities that occur under your account. You agree to notify us immediately of
                    any unauthorized use of your account or any other breach of security.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">3.3 Account Termination</h3>
                  <p className="text-tana-muted leading-relaxed">
                    You may terminate your account at any time by following the account deletion
                    process. We reserve the right to suspend or terminate your account for
                    violations of these Terms or for any other reason at our sole discretion.
                  </p>
                </div>
              </div>
            </section>

            {/* Acceptable Use */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">4. Acceptable Use</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">4.1 Permitted Uses</h3>
                  <p className="text-tana-muted leading-relaxed mb-4">
                    You may use our Service for lawful purposes and in accordance with these Terms.
                    You are encouraged to:
                  </p>
                  <ul className="space-y-2 text-tana-muted list-disc list-inside">
                    <li>Use the Service for personal and commercial purposes</li>
                    <li>Import and analyze your own Tana workspace data</li>
                    <li>Create AI-powered conversations and workflows</li>
                    <li>Develop integrations using our API and MCP server</li>
                    <li>Provide feedback and suggestions to improve the Service</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">
                    4.2 Prohibited Activities
                  </h3>
                  <p className="text-tana-muted leading-relaxed mb-4">
                    You agree not to engage in any of the following prohibited activities:
                  </p>
                  <ul className="space-y-2 text-tana-muted list-disc list-inside">
                    <li>
                      <strong>Illegal Activities:</strong> Using the Service for any illegal
                      purposes or to violate any laws
                    </li>
                    <li>
                      <strong>Intellectual Property:</strong> Infringing on copyrights, trademarks,
                      patents, or other intellectual property rights
                    </li>
                    <li>
                      <strong>Security Breaches:</strong> Attempting to gain unauthorized access to
                      our systems or other users' data
                    </li>
                    <li>
                      <strong>Spam and Abuse:</strong> Sending unsolicited communications, engaging
                      in harassment, or creating misleading content
                    </li>
                    <li>
                      <strong>Data Misuse:</strong> Using another person's data without consent or
                      violating data privacy regulations
                    </li>
                    <li>
                      <strong>Reverse Engineering:</strong> Attempting to reverse engineer,
                      decompile, or disassemble any aspect of the Service
                    </li>
                    <li>
                      <strong>Competitive Use:</strong> Using our Service to create a competing
                      product or service
                    </li>
                    <li>
                      <strong>System Abuse:</strong> Overloading our systems with excessive requests
                      or automated access
                    </li>
                  </ul>
                </div>
              </div>
            </section>

            {/* Intellectual Property Rights */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">
                5. Intellectual Property Rights
              </h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">
                    5.1 Our Intellectual Property
                  </h3>
                  <p className="text-tana-muted leading-relaxed">
                    The Service and its original content, features, and functionality are and will
                    remain the exclusive property of TanaChat.ai and its licensors. The Service is
                    protected by copyright, trademark, and other laws.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">5.2 Your Content</h3>
                  <p className="text-tana-muted leading-relaxed mb-4">
                    You retain ownership of any content you create or upload to our Service,
                    including:
                  </p>
                  <ul className="space-y-2 text-tana-muted list-disc list-inside">
                    <li>Your chat conversations and AI-generated responses</li>
                    <li>Your Tana workspace data and imported content</li>
                    <li>Any custom workflows or integrations you create</li>
                  </ul>
                  <p className="text-tana-muted leading-relaxed mt-3">
                    By providing content to our Service, you grant us a worldwide, non-exclusive,
                    royalty-free license to use, process, and store your content solely for the
                    purpose of providing and improving the Service.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">
                    5.3 Open Source Components
                  </h3>
                  <p className="text-tana-muted leading-relaxed">
                    Our Service incorporates open source software components. These components are
                    subject to their respective license terms, which are available upon request or
                    included in our documentation.
                  </p>
                </div>
              </div>
            </section>

            {/* AI Services and Third-Party Providers */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">
                6. AI Services and Third-Party Providers
              </h2>

              <div className="space-y-4 text-tana-muted">
                <p>
                  Our Service integrates with third-party AI providers to generate responses and
                  process your requests. These include:
                </p>
                <ul className="space-y-2 list-disc list-inside">
                  <li>
                    <strong>Anthropic/Claude:</strong> For advanced reasoning and complex task
                    completion
                  </li>
                  <li>
                    <strong>OpenAI/ChatGPT:</strong> For creative writing and conversational AI
                    capabilities
                  </li>
                </ul>
                <p>
                  Your use of these AI services is subject to the respective terms of service and
                  privacy policies of these providers. We are not responsible for the content
                  generated by these AI services, and you acknowledge that AI-generated content may
                  be inaccurate, incomplete, or offensive.
                </p>
              </div>
            </section>

            {/* Privacy and Data Protection */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">7. Privacy and Data Protection</h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                Your privacy is important to us. Please review our Privacy Policy, which also
                governs your use of the Service, to understand our practices.
              </p>
              <div className="bg-tana-bg/50 rounded-lg p-4 space-y-2 text-tana-muted">
                <p>Key points:</p>
                <ul className="space-y-2 list-disc list-inside">
                  <li>We collect and process your data as described in our Privacy Policy</li>
                  <li>Your chat history may be processed by third-party AI providers</li>
                  <li>We implement security measures to protect your data</li>
                  <li>
                    You have rights regarding your personal data as described in our Privacy Policy
                  </li>
                </ul>
              </div>
            </section>

            {/* Paid Services and Billing */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">8. Paid Services and Billing</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">8.1 Service Tiers</h3>
                  <p className="text-tana-muted leading-relaxed">
                    We offer both free and paid service tiers. Free users have access to basic
                    features with usage limitations. Paid tiers provide enhanced features, higher
                    usage limits, and priority support.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">8.2 Billing Terms</h3>
                  <ul className="space-y-2 text-tana-muted list-disc list-inside">
                    <li>Payments are processed through our third-party payment providers</li>
                    <li>Subscription fees are billed in advance on a recurring basis</li>
                    <li>All fees are non-refundable except as required by law</li>
                    <li>We may change our pricing with 30 days' notice for existing subscribers</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">8.3 Usage Limits</h3>
                  <p className="text-tana-muted leading-relaxed">
                    Each service tier has specific usage limits for API calls, chat messages, and
                    data storage. Exceeding these limits may result in additional charges or service
                    restrictions.
                  </p>
                </div>
              </div>
            </section>

            {/* Disclaimer of Warranties */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">9. Disclaimer of Warranties</h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTY OF ANY KIND,
                EITHER EXPRESS OR IMPLIED. WE DISCLAIM ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO:
              </p>
              <ul className="space-y-2 text-tana-muted list-disc list-inside">
                <li>
                  <strong>Accuracy:</strong> We do not guarantee the accuracy or reliability of
                  AI-generated content
                </li>
                <li>
                  <strong>Availability:</strong> The Service may be temporarily unavailable for
                  maintenance or technical reasons
                </li>
                <li>
                  <strong>Compatibility:</strong> We do not guarantee compatibility with all
                  devices, browsers, or systems
                </li>
                <li>
                  <strong>Security:</strong> While we implement security measures, we cannot
                  guarantee absolute security
                </li>
                <li>
                  <strong>Fitness:</strong> We do not guarantee the Service will meet your specific
                  requirements
                </li>
              </ul>
            </section>

            {/* Limitation of Liability */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">10. Limitation of Liability</h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                TO THE MAXIMUM EXTENT PERMITTED BY LAW, TANACHAT.AI SHALL NOT BE LIABLE FOR ANY
                INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT
                LIMITED TO:
              </p>
              <ul className="space-y-2 text-tana-muted list-disc list-inside mb-4">
                <li>Loss of data, revenue, or profits</li>
                <li>Business interruption or loss of opportunity</li>
                <li>Damage to reputation or goodwill</li>
                <li>Costs of procurement of substitute goods or services</li>
              </ul>
              <p className="text-tana-muted leading-relaxed">
                Our total liability for any claims arising out of or relating to these Terms or the
                Service shall not exceed the amount you paid us in the twelve (12) months preceding
                the claim.
              </p>
            </section>

            {/* Indemnification */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">11. Indemnification</h2>
              <p className="text-tana-muted leading-relaxed">
                You agree to indemnify and hold TanaChat.ai and its officers, directors, employees,
                and agents harmless from any and all claims, liabilities, damages, losses, and
                expenses, including reasonable attorneys' fees, arising from:
              </p>
              <ul className="space-y-2 text-tana-muted list-disc list-inside">
                <li>Your use of the Service</li>
                <li>Your violation of these Terms</li>
                <li>Your violation of any rights of another person or entity</li>
                <li>Your violation of applicable laws or regulations</li>
              </ul>
            </section>

            {/* Termination */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">12. Termination</h2>

              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">12.1 Termination by You</h3>
                  <p className="text-tana-muted leading-relaxed">
                    You may terminate your account and use of the Service at any time by following
                    the account deletion process or by contacting us.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">12.2 Termination by Us</h3>
                  <p className="text-tana-muted leading-relaxed">
                    We may terminate or suspend your account and access to the Service at our sole
                    discretion, without prior notice or liability, for any reason, including but not
                    limited to:
                  </p>
                  <ul className="space-y-2 text-tana-muted list-disc list-inside mt-3">
                    <li>Breach of these Terms</li>
                    <li>Violation of applicable laws</li>
                    <li>Fraudulent or illegal activity</li>
                    <li>Extended inactivity</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">
                    12.3 Effect of Termination
                  </h3>
                  <p className="text-tana-muted leading-relaxed">
                    Upon termination, your right to use the Service will cease immediately. We may
                    delete your account and data, except where we are required to retain it by law.
                    Sections that by their nature should survive termination will survive.
                  </p>
                </div>
              </div>
            </section>

            {/* Governing Law */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">
                13. Governing Law and Dispute Resolution
              </h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                These Terms shall be governed by and construed in accordance with the laws of the
                jurisdiction where TanaChat.ai operates, without regard to its conflict of law
                provisions.
              </p>
              <p className="text-tana-muted leading-relaxed mb-4">
                Any dispute arising out of or relating to these Terms or the Service shall be
                resolved through:
              </p>
              <ol className="space-y-2 text-tana-muted list-decimal list-inside">
                <li>Good faith negotiation between the parties</li>
                <li>Mediation with a neutral third-party mediator</li>
                <li>Binding arbitration as a last resort</li>
              </ol>
              <p className="text-tana-muted leading-relaxed">
                You agree to waive any right to a jury trial and to bring any claim in an individual
                capacity.
              </p>
            </section>

            {/* Changes to Terms */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">14. Changes to These Terms</h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                We reserve the right to modify these Terms at any time. When we make changes, we
                will:
              </p>
              <ul className="space-y-2 text-tana-muted list-disc list-inside">
                <li>Post the updated Terms on our website</li>
                <li>Update the "Last updated" date</li>
                <li>Notify users of material changes via email or in-app notification</li>
                <li>Provide a reasonable period for users to review the changes</li>
              </ul>
              <p className="text-tana-muted leading-relaxed">
                Your continued use of the Service after any changes constitutes acceptance of the
                updated Terms.
              </p>
            </section>

            {/* General Provisions */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">15. General Provisions</h2>

              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">15.1 Entire Agreement</h3>
                  <p className="text-tana-muted leading-relaxed">
                    These Terms, together with our Privacy Policy and any other legal notices
                    published on our Service, constitute the entire agreement between you and
                    TanaChat.ai.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">15.2 Severability</h3>
                  <p className="text-tana-muted leading-relaxed">
                    If any provision of these Terms is held to be unenforceable or invalid, such
                    provision will be changed and interpreted to accomplish the objectives of such
                    provision to the greatest extent possible under applicable law.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">15.3 No Waiver</h3>
                  <p className="text-tana-muted leading-relaxed">
                    Our failure to enforce any right or provision of these Terms will not be
                    considered a waiver of those rights.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">15.4 Assignment</h3>
                  <p className="text-tana-muted leading-relaxed">
                    You may not assign or transfer these Terms without our prior written consent. We
                    may assign or transfer these Terms without restriction.
                  </p>
                </div>
              </div>
            </section>

            {/* Contact Information */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">16. Contact Information</h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                If you have any questions about these Terms of Service, please contact us:
              </p>
              <div className="bg-tana-bg/50 rounded-lg p-4 space-y-2 text-tana-muted">
                <p>
                  <strong>Email:</strong> legal@tanachat.ai
                </p>
                <p>
                  <strong>Website:</strong> https://tanachat.ai
                </p>
                <p>
                  <strong>GitHub:</strong> https://github.com/thomashaus/TanaChat
                </p>
                <p>
                  <strong>Documentation:</strong> https://api.tanachat.ai/docs
                </p>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}
