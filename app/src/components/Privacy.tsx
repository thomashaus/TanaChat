import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { BackgroundGraph } from './BackgroundGraph';

export function Privacy() {
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
              to="/terms"
              className="text-sm font-medium text-tana-muted hover:text-white transition-colors"
            >
              Terms
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
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
                Privacy Policy
              </span>
            </h1>
            <p className="text-tana-muted text-lg">
              Protecting your data and privacy is fundamental to how we operate.
            </p>
            <p className="text-tana-muted text-sm mt-2">Last updated: {lastUpdated}</p>
          </div>

          {/* Content Sections */}
          <div className="space-y-12">
            {/* Introduction */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">1. Introduction</h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                TanaChat.ai ("we," "us," or "our") is committed to protecting your privacy. This
                Privacy Policy explains how we collect, use, disclose, and safeguard your
                information when you use our service, including our web application, API services,
                and MCP (Model Context Protocol) server integrations.
              </p>
              <p className="text-tana-muted leading-relaxed">
                By using TanaChat.ai, you consent to the data practices described in this policy. If
                you do not agree with the terms of this privacy policy, please do not access or use
                our service.
              </p>
            </section>

            {/* Information We Collect */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">2. Information We Collect</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">
                    2.1 Information You Provide
                  </h3>
                  <ul className="space-y-2 text-tana-muted list-disc list-inside">
                    <li>
                      <strong>Account Information:</strong> Name, email address, and authentication
                      credentials when you create an account
                    </li>
                    <li>
                      <strong>Chat Content:</strong> Messages, prompts, and conversations you have
                      with AI models
                    </li>
                    <li>
                      <strong>Tana Workspace Data:</strong> Node structures, field data, and
                      connections you import from Tana
                    </li>
                    <li>
                      <strong>CLI Usage Data:</strong> Commands executed and files processed through
                      our CLI tools
                    </li>
                    <li>
                      <strong>Communications:</strong> Support requests, feedback, and other
                      communications with us
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">
                    2.2 Automatically Collected Information
                  </h3>
                  <ul className="space-y-2 text-tana-muted list-disc list-inside">
                    <li>
                      <strong>Usage Data:</strong> Pages visited, time spent, features used, and
                      interaction patterns
                    </li>
                    <li>
                      <strong>Log Data:</strong> IP addresses, browser types, device information,
                      and timestamps
                    </li>
                    <li>
                      <strong>Performance Data:</strong> Response times, error rates, and system
                      performance metrics
                    </li>
                    <li>
                      <strong>API Usage:</strong> Request counts, response sizes, and integration
                      usage patterns
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">
                    2.3 Cookies and Tracking Technologies
                  </h3>
                  <p className="text-tana-muted leading-relaxed mb-3">
                    We use cookies and similar technologies to:
                  </p>
                  <ul className="space-y-2 text-tana-muted list-disc list-inside">
                    <li>Authenticate users and maintain sessions</li>
                    <li>Remember user preferences and settings</li>
                    <li>Analyze service usage and performance</li>
                    <li>Provide security and fraud protection</li>
                  </ul>
                </div>
              </div>
            </section>

            {/* How We Use Your Information */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">3. How We Use Your Information</h2>

              <div className="space-y-4 text-tana-muted">
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 rounded-full bg-indigo-500 mt-2 flex-shrink-0"></div>
                  <div>
                    <strong>Service Provision:</strong> To provide, maintain, and improve our
                    AI-powered chat services and Tana integration features
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 rounded-full bg-indigo-500 mt-2 flex-shrink-0"></div>
                  <div>
                    <strong>Personalization:</strong> To customize your experience and provide
                    relevant AI responses based on your Tana workspace data
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 rounded-full bg-indigo-500 mt-2 flex-shrink-0"></div>
                  <div>
                    <strong>Communication:</strong> To respond to your inquiries, provide support,
                    and send important service updates
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 rounded-full bg-indigo-500 mt-2 flex-shrink-0"></div>
                  <div>
                    <strong>Analytics:</strong> To analyze usage patterns, improve service
                    performance, and develop new features
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 rounded-full bg-indigo-500 mt-2 flex-shrink-0"></div>
                  <div>
                    <strong>Security:</strong> To detect and prevent fraud, abuse, and security
                    threats
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 rounded-full bg-indigo-500 mt-2 flex-shrink-0"></div>
                  <div>
                    <strong>Legal Compliance:</strong> To comply with legal obligations and enforce
                    our terms of service
                  </div>
                </div>
              </div>
            </section>

            {/* Information Sharing */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">
                4. Information Sharing and Disclosure
              </h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">
                    4.1 Third-Party AI Providers
                  </h3>
                  <p className="text-tana-muted leading-relaxed">
                    Your chat messages may be processed by third-party AI providers
                    (Claude/Anthropic, OpenAI/ChatGPT) to generate responses. These providers have
                    their own privacy policies and data handling practices.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">4.2 Service Providers</h3>
                  <p className="text-tana-muted leading-relaxed">
                    We may share information with trusted third-party service providers who perform
                    services on our behalf, including:
                  </p>
                  <ul className="space-y-2 text-tana-muted list-disc list-inside mt-3">
                    <li>Cloud hosting and infrastructure services</li>
                    <li>Analytics and monitoring services</li>
                    <li>Customer support platforms</li>
                    <li>Security and fraud prevention services</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">4.3 Legal Requirements</h3>
                  <p className="text-tana-muted leading-relaxed">
                    We may disclose your information if required by law, court order, or government
                    request, or to protect our rights, property, or safety, or that of our users or
                    the public.
                  </p>
                </div>
              </div>
            </section>

            {/* Data Security */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">5. Data Security</h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                We implement appropriate technical and organizational measures to protect your
                information, including:
              </p>
              <ul className="space-y-2 text-tana-muted list-disc list-inside">
                <li>End-to-end encryption for data in transit using TLS 1.3+</li>
                <li>Encryption at rest using industry-standard encryption algorithms</li>
                <li>Regular security audits and penetration testing</li>
                <li>Access controls and authentication mechanisms</li>
                <li>Secure development practices and code reviews</li>
              </ul>
              <p className="text-tana-muted leading-relaxed mt-4">
                However, no method of transmission over the internet or electronic storage is 100%
                secure. While we strive to use commercially acceptable means to protect your
                personal information, we cannot guarantee its absolute security.
              </p>
            </section>

            {/* Data Retention */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">6. Data Retention</h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                We retain your information for as long as necessary to provide our services, comply
                with legal obligations, resolve disputes, and enforce our agreements:
              </p>
              <ul className="space-y-2 text-tana-muted list-disc list-inside">
                <li>
                  <strong>Chat History:</strong> Retained for 365 days from creation date, unless
                  you delete it sooner
                </li>
                <li>
                  <strong>Account Information:</strong> Retained while your account is active
                </li>
                <li>
                  <strong>Usage Logs:</strong> Retained for 90 days for security and performance
                  analysis
                </li>
                <li>
                  <strong>Deleted Data:</strong> Permanently deleted within 30 days of deletion
                  request
                </li>
              </ul>
            </section>

            {/* Your Rights */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">7. Your Privacy Rights</h2>

              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">
                    7.1 Access and Correction
                  </h3>
                  <p className="text-tana-muted leading-relaxed">
                    You have the right to access and update your personal information through your
                    account settings or by contacting us directly.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">7.2 Data Deletion</h3>
                  <p className="text-tana-muted leading-relaxed">
                    You can request deletion of your account and associated data at any time. We
                    will delete your information within 30 days, except where we're required to
                    retain it for legal or legitimate business purposes.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">7.3 Data Portability</h3>
                  <p className="text-tana-muted leading-relaxed">
                    You can request a copy of your data in a structured, machine-readable format. We
                    provide export functionality for chat history and workspace data.
                  </p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-3 text-white">7.4 Opt-Out Rights</h3>
                  <p className="text-tana-muted leading-relaxed">
                    You can opt out of non-essential data collection and processing through your
                    account preferences or by adjusting browser settings.
                  </p>
                </div>
              </div>
            </section>

            {/* International Data Transfers */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">
                8. International Data Transfers
              </h2>
              <p className="text-tana-muted leading-relaxed">
                Your information may be transferred to and processed in countries other than your
                own. When we transfer your information internationally, we ensure appropriate
                safeguards are in place to protect your privacy rights, including standard
                contractual clauses or other legally recognized mechanisms.
              </p>
            </section>

            {/* Children's Privacy */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">9. Children's Privacy</h2>
              <p className="text-tana-muted leading-relaxed">
                Our service is not intended for children under 13 years of age. We do not knowingly
                collect personal information from children under 13. If we become aware that we have
                collected personal information from a child under 13, we will take steps to delete
                such information immediately.
              </p>
            </section>

            {/* Changes to This Policy */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">
                10. Changes to This Privacy Policy
              </h2>
              <p className="text-tana-muted leading-relaxed">
                We may update this Privacy Policy from time to time. We will notify you of any
                changes by posting the new policy on this page and updating the "Last updated" date.
                Continued use of our service after any changes constitutes acceptance of the updated
                policy.
              </p>
            </section>

            {/* Contact Information */}
            <section className="rounded-2xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
              <h2 className="text-2xl font-bold mb-4 text-white">11. Contact Us</h2>
              <p className="text-tana-muted leading-relaxed mb-4">
                If you have any questions about this Privacy Policy or our data practices, please
                contact us:
              </p>
              <div className="bg-tana-bg/50 rounded-lg p-4 space-y-2 text-tana-muted">
                <p>
                  <strong>Email:</strong> privacy@tanachat.ai
                </p>
                <p>
                  <strong>Website:</strong> https://tanachat.ai
                </p>
                <p>
                  <strong>GitHub:</strong> https://github.com/thomashaus/TanaChat
                </p>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}
