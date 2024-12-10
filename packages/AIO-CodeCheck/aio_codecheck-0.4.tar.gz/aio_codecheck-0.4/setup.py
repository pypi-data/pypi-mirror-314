from setuptools import setup, find_packages

setup(
    name='AIO-CodeCheck',  # نام پکیج شما
    version='0.4',  # نسخه جاری پکیج (در صورت آپدیت تغییر دهید)
    packages=find_packages(),
    install_requires=[
        'rich',  # کتابخانه rich برای ایجاد رابط کاربری
    ],
    entry_points={
        'console_scripts': [
            'aio-check = aio_check.check:main',  # پیکربندی برای اجرای اسکریپت از خط فرمان
        ],
    },
    author='MOBIN_YM',
    author_email='yaghoobi.m191@gmail.com',  # ایمیل نویسنده پروژه
    description='A simple Python code evaluation tool.',  # توضیح کوتاه در مورد پروژه
    long_description=open('README.md').read(),  # توضیحات طولانی از فایل README
    long_description_content_type='text/markdown',  # نوع محتوا برای فایل README
    url='https://github.com/mobinym/AIO_CodeCheck',  # لینک به صفحه پروژه در GitHub
    classifiers=[
        'Programming Language :: Python :: 3',  # زبان‌های پشتیبانی شده
        'License :: OSI Approved :: MIT License',  # نوع مجوز
        'Operating System :: OS Independent',  # پشتیبانی از سیستم‌های عامل مختلف
    ],
    python_requires='>=3.6',  # نسخه‌های پایتون پشتیبانی شده
)
