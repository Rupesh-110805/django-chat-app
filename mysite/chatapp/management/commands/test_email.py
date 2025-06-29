from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def add_arguments(self, parser):
        parser.add_argument('--to', type=str, help='Email address to send test email to', required=True)

    def handle(self, *args, **options):
        recipient_email = options['to']
        
        self.stdout.write(f'📧 Testing email configuration...')
        self.stdout.write(f'   From: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'   To: {recipient_email}')
        self.stdout.write(f'   Backend: {settings.EMAIL_BACKEND}')
        
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
            self.stdout.write(
                self.style.WARNING('⚠️  Using console backend - emails will appear in terminal only')
            )
        else:
            self.stdout.write(f'   SMTP Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
        
        try:
            send_mail(
                subject='🧪 Test Email from Django Chat App',
                message='This is a test email to verify that email configuration is working correctly.\n\nIf you received this email, your Django app can send real emails! 🎉',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False,
            )
            
            if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
                self.stdout.write(
                    self.style.SUCCESS('✅ Email sent to console (check terminal output above)')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Real email sent successfully to {recipient_email}!')
                )
                self.stdout.write('📬 Check your inbox (and spam folder) for the test email.')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send email: {str(e)}')
            )
            
            if 'authentication failed' in str(e).lower():
                self.stdout.write('')
                self.stdout.write(self.style.WARNING('� Authentication Error - Check these:'))
                self.stdout.write('   1. Gmail email address is correct')
                self.stdout.write('   2. App password is correct (16 characters)')
                self.stdout.write('   3. 2-step verification is enabled')
                self.stdout.write('   4. App password was generated for "Mail"')
            elif 'connection' in str(e).lower():
                self.stdout.write('')
                self.stdout.write(self.style.WARNING('🌐 Connection Error - Check these:'))
                self.stdout.write('   1. Internet connection is working')
                self.stdout.write('   2. Firewall/antivirus not blocking SMTP')
                self.stdout.write('   3. Gmail SMTP settings are correct')
            else:
                self.stdout.write('')
                self.stdout.write(self.style.WARNING('💡 Make sure your email settings are configured correctly in .env file'))
                
        self.stdout.write('')
        self.stdout.write('📋 Current email settings:')
        self.stdout.write(f'   EMAIL_BACKEND = {settings.EMAIL_BACKEND}')
        self.stdout.write(f'   EMAIL_HOST = {getattr(settings, "EMAIL_HOST", "Not set")}')
        self.stdout.write(f'   EMAIL_PORT = {getattr(settings, "EMAIL_PORT", "Not set")}')
        self.stdout.write(f'   EMAIL_USE_TLS = {getattr(settings, "EMAIL_USE_TLS", "Not set")}')
        self.stdout.write(f'   EMAIL_HOST_USER = {getattr(settings, "EMAIL_HOST_USER", "Not set")}')
        self.stdout.write(f'   DEFAULT_FROM_EMAIL = {getattr(settings, "DEFAULT_FROM_EMAIL", "Not set")}')
