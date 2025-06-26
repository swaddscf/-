#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕌 تطبيق أوقات الصلاة المتقدم - نسخة محسنة 🕌
Advanced Prayer Times Application - Enhanced Version

المكتبات المستخدمة:
✅ tkinter - واجهة المستخدم الرسومية (مدمجة مع Python)
✅ requests - للاتصال بـ APIs (اختيارية)
✅ urllib - بديل requests (مدمج مع Python)
✅ json - لمعالجة البيانات وحفظ الإعدادات
✅ threading - للعمليات المتوازية
✅ datetime - للتعامل مع التاريخ والوقت
✅ math - للحسابات الفلكية
✅ webbrowser - لفتح الروابط
✅ os - للتعامل مع الملفات

المميزات:
🌍 تحديد الموقع تلقائياً
🌤️ معلومات الطقس الحية
🧭 حساب اتجاه القبلة
📅 التاريخ الهجري
📊 إحصائيات الصلاة
🔔 تنبيهات ذكية
🎨 تصميم حديث وجذاب

الإصدار: 2.0
المطور: مساعد الذكي
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import math
import json
import threading
import webbrowser
import os
import urllib.request
import urllib.parse
import urllib.error
import random

# محاولة استيراد المكتبات الاختيارية
try:
    import requests
    REQUESTS_AVAILABLE = True
    print("✅ مكتبة requests متوفرة")
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️ مكتبة requests غير متوفرة - سيتم استخدام urllib")

class PrayerTimesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕌 أوقات الصلاة المتقدم - Advanced Prayer Times 🕌")
        self.root.geometry("800x900")
        self.root.configure(bg='#0f172a')
        self.root.resizable(True, True)
        
        # إعداد أيقونة التطبيق (اختيارية)
        try:
            self.root.iconbitmap(default='mosque.ico')
        except:
            pass
        
        # متغيرات التطبيق الأساسية
        self.city = tk.StringVar(value="الرياض")
        self.country = tk.StringVar(value="السعودية")
        self.latitude = tk.DoubleVar(value=24.7136)
        self.longitude = tk.DoubleVar(value=46.6753)
        self.prayer_times = {}
        self.current_time = tk.StringVar()
        self.next_prayer = tk.StringVar()
        self.time_to_next = tk.StringVar()
        
        # متغيرات المعلومات الإضافية
        self.weather_info = tk.StringVar(value="🌤️ جاري تحميل الطقس...")
        self.location_info = tk.StringVar(value="📍 الرياض، السعودية")
        self.qibla_direction = tk.StringVar(value="🧭 جاري حساب اتجاه القبلة...")
        self.islamic_date = tk.StringVar(value="📅 جاري تحميل التاريخ الهجري...")
        self.prayer_counter = tk.StringVar(value="📊 0/5 صلوات اليوم")
        
        # متغيرات الإعدادات
        self.notification_enabled = tk.BooleanVar(value=True)
        self.sound_enabled = tk.BooleanVar(value=True)
        self.auto_location = tk.BooleanVar(value=True)
        self.show_weather = tk.BooleanVar(value=True)
        
        # إحصائيات الصلاة
        self.prayers_completed_today = 0
        self.total_prayers_month = 0
        self.streak_days = 0
        
        # إعدادات التطبيق
        self.settings = {
            'calculation_method': 4,  # أم القرى
            'auto_location': True,
            'show_weather': True,
            'notifications': True,
            'sounds': True
        }
        
        # ألوان وأيقونات الصلوات
        self.prayer_colors = {
            'الفجر': '#1e40af',
            'الشروق': '#f59e0b', 
            'الظهر': '#dc2626',
            'العصر': '#ea580c',
            'المغرب': '#7c3aed',
            'العشاء': '#1e293b'
        }
        
        self.prayer_icons = {
            'الفجر': '🌅',
            'الشروق': '☀️',
            'الظهر': '🌞', 
            'العصر': '🌇',
            'المغرب': '🌆',
            'العشاء': '🌙'
        }
        
        # تحميل الإعدادات والبيانات المحفوظة
        self.load_settings()
        self.load_prayer_statistics()
        
        # إعداد الواجهة
        self.setup_ui()
        
        # بدء العمليات
        self.start_operations()
    
    def load_settings(self):
        """تحميل الإعدادات المحفوظة"""
        try:
            if os.path.exists('prayer_settings.json'):
                with open('prayer_settings.json', 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    self.settings.update(saved_settings)
                    print("✅ تم تحميل الإعدادات")
        except Exception as e:
            print(f"⚠️ خطأ في تحميل الإعدادات: {e}")
    
    def save_settings(self):
        """حفظ الإعدادات"""
        try:
            with open('prayer_settings.json', 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
                print("✅ تم حفظ الإعدادات")
        except Exception as e:
            print(f"⚠️ خطأ في حفظ الإعدادات: {e}")
    
    def load_prayer_statistics(self):
        """تحميل إحصائيات الصلاة"""
        try:
            if os.path.exists('prayer_stats.json'):
                with open('prayer_stats.json', 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                    self.prayers_completed_today = stats.get('today', 0)
                    self.total_prayers_month = stats.get('month', 0)
                    self.streak_days = stats.get('streak', 0)
                    print("✅ تم تحميل الإحصائيات")
            self.update_prayer_counter()
        except Exception as e:
            print(f"⚠️ خطأ في تحميل الإحصائيات: {e}")
    
    def save_prayer_statistics(self):
        """حفظ إحصائيات الصلاة"""
        try:
            stats = {
                'today': self.prayers_completed_today,
                'month': self.total_prayers_month,
                'streak': self.streak_days,
                'last_update': datetime.now().isoformat()
            }
            with open('prayer_stats.json', 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ خطأ في حفظ الإحصائيات: {e}")
    
    def update_prayer_counter(self):
        """تحديث عداد الصلوات"""
        self.prayer_counter.set(f"📊 {self.prayers_completed_today}/5 صلوات اليوم")
    
    def start_operations(self):
        """بدء العمليات الأساسية"""
        # تحديث الوقت
        self.update_time()
        
        # حساب اتجاه القبلة
        self.calculate_qibla_direction()
        
        # جلب التاريخ الهجري
        self.get_islamic_date()
        
        # تحديد الموقع أو حساب الأوقات
        if self.settings.get('auto_location', True):
            self.detect_location()
        else:
            self.get_prayer_times()
        
        # جلب معلومات الطقس
        if self.settings.get('show_weather', True):
            self.get_weather_info()
        
        # بدء التحديثات الدورية
        self.schedule_updates()
    
    def detect_location(self):
        """تحديد الموقع الجغرافي تلقائياً"""
        def get_location():
            try:
                print("🔍 جاري تحديد الموقع...")
                
                # استخدام خدمة مجانية لتحديد الموقع
                url = 'http://ip-api.com/json/?lang=ar'
                
                if REQUESTS_AVAILABLE:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if data['status'] == 'success':
                            self.process_location_data(data)
                            return
                
                # استخدام urllib كبديل
                with urllib.request.urlopen(url, timeout=10) as response:
                    data = json.loads(response.read().decode())
                    if data['status'] == 'success':
                        self.process_location_data(data)
                    else:
                        self.use_default_location()
                        
            except Exception as e:
                print(f"⚠️ خطأ في تحديد الموقع: {e}")
                self.use_default_location()
        
        threading.Thread(target=get_location, daemon=True).start()
    
    def process_location_data(self, data):
        """معالجة بيانات الموقع"""
        try:
            self.latitude.set(data['lat'])
            self.longitude.set(data['lon'])
            self.city.set(data['city'])
            self.country.set(data['country'])
            self.location_info.set(f"📍 {data['city']}, {data['country']}")
            
            print(f"✅ تم تحديد الموقع: {data['city']}, {data['country']}")
            
            # تحديث البيانات المعتمدة على الموقع
            self.root.after(0, self.get_prayer_times)
            self.root.after(0, self.get_weather_info)
            self.root.after(0, self.calculate_qibla_direction)
            
        except Exception as e:
            print(f"⚠️ خطأ في معالجة بيانات الموقع: {e}")
            self.use_default_location()
    
    def use_default_location(self):
        """استخدام الموقع الافتراضي (الرياض)"""
        self.latitude.set(24.7136)
        self.longitude.set(46.6753)
        self.city.set("الرياض")
        self.country.set("السعودية")
        self.location_info.set("📍 الرياض, السعودية (افتراضي)")
        print("📍 تم استخدام الرياض كموقع افتراضي")
        
        # تحديث البيانات
        self.root.after(0, self.get_prayer_times)
        self.root.after(0, self.get_weather_info)
        self.root.after(0, self.calculate_qibla_direction)

    def get_weather_info(self):
        """الحصول على معلومات الطقس"""
        def fetch_weather():
            try:
                lat = self.latitude.get()
                lon = self.longitude.get()

                # استخدام Open-Meteo API (مجاني 100%)
                url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"

                if REQUESTS_AVAILABLE:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        self.process_weather_data(data)
                        return

                # استخدام urllib كبديل
                with urllib.request.urlopen(url, timeout=10) as response:
                    data = json.loads(response.read().decode())
                    self.process_weather_data(data)

            except Exception as e:
                print(f"⚠️ خطأ في جلب الطقس: {e}")
                self.weather_info.set("🌤️ 25°C | صافي ☀️ (تقديري)")

        threading.Thread(target=fetch_weather, daemon=True).start()

    def process_weather_data(self, data):
        """معالجة بيانات الطقس"""
        try:
            current = data.get('current_weather', {})
            temp = current.get('temperature', 'N/A')
            weather_code = current.get('weathercode', 0)
            weather_desc = self.get_weather_description(weather_code)

            weather_text = f"🌡️ {temp}°C | {weather_desc}"
            self.weather_info.set(weather_text)
            print(f"✅ تم تحديث الطقس: {weather_text}")

        except Exception as e:
            print(f"⚠️ خطأ في معالجة بيانات الطقس: {e}")
            self.weather_info.set("🌤️ الطقس غير متوفر")

    def get_weather_description(self, code):
        """تحويل رمز الطقس إلى وصف عربي"""
        weather_codes = {
            0: "صافي ☀️",
            1: "صافي جزئياً 🌤️",
            2: "غائم جزئياً ⛅",
            3: "غائم ☁️",
            45: "ضباب 🌫️",
            48: "ضباب متجمد 🌫️",
            51: "رذاذ خفيف 🌦️",
            53: "رذاذ متوسط 🌦️",
            55: "رذاذ كثيف 🌦️",
            61: "مطر خفيف 🌧️",
            63: "مطر متوسط 🌧️",
            65: "مطر غزير ⛈️",
            71: "ثلج خفيف ❄️",
            73: "ثلج متوسط ❄️",
            75: "ثلج كثيف ❄️",
            95: "عاصفة رعدية ⛈️"
        }
        return weather_codes.get(code, "غير محدد 🌈")

    def calculate_qibla_direction(self):
        """حساب اتجاه القبلة من الموقع الحالي"""
        try:
            # إحداثيات الكعبة المشرفة
            kaaba_lat = 21.4225
            kaaba_lon = 39.8262

            # إحداثيات الموقع الحالي
            lat = math.radians(self.latitude.get())
            lon = math.radians(self.longitude.get())
            kaaba_lat_rad = math.radians(kaaba_lat)
            kaaba_lon_rad = math.radians(kaaba_lon)

            # حساب الاتجاه باستخدام الصيغة الكروية
            dlon = kaaba_lon_rad - lon
            y = math.sin(dlon) * math.cos(kaaba_lat_rad)
            x = math.cos(lat) * math.sin(kaaba_lat_rad) - math.sin(lat) * math.cos(kaaba_lat_rad) * math.cos(dlon)

            # تحويل إلى درجات
            bearing = math.atan2(y, x)
            bearing = math.degrees(bearing)
            bearing = (bearing + 360) % 360

            # تحديد الاتجاه النصي
            directions = [
                "شمال", "شمال شرق", "شرق", "جنوب شرق",
                "جنوب", "جنوب غرب", "غرب", "شمال غرب"
            ]
            direction_index = round(bearing / 45) % 8
            direction_text = directions[direction_index]

            self.qibla_direction.set(f"🧭 القبلة: {direction_text} ({bearing:.1f}°)")
            print(f"✅ تم حساب اتجاه القبلة: {direction_text}")

        except Exception as e:
            print(f"⚠️ خطأ في حساب اتجاه القبلة: {e}")
            self.qibla_direction.set("🧭 القبلة: غير محدد")

    def get_islamic_date(self):
        """الحصول على التاريخ الهجري"""
        def fetch_islamic_date():
            try:
                today = datetime.now().strftime("%d-%m-%Y")
                url = f"http://api.aladhan.com/v1/gToH/{today}"

                if REQUESTS_AVAILABLE:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        self.process_islamic_date(data)
                        return

                # استخدام urllib كبديل
                with urllib.request.urlopen(url, timeout=10) as response:
                    data = json.loads(response.read().decode())
                    self.process_islamic_date(data)

            except Exception as e:
                print(f"⚠️ خطأ في جلب التاريخ الهجري: {e}")
                self.islamic_date.set("📅 التاريخ الهجري غير متوفر")

        threading.Thread(target=fetch_islamic_date, daemon=True).start()

    def process_islamic_date(self, data):
        """معالجة بيانات التاريخ الهجري"""
        try:
            hijri = data['data']['hijri']
            hijri_date = f"{hijri['day']} {hijri['month']['ar']} {hijri['year']} هـ"
            self.islamic_date.set(f"📅 {hijri_date}")
            print(f"✅ تم تحديث التاريخ الهجري: {hijri_date}")
        except Exception as e:
            print(f"⚠️ خطأ في معالجة التاريخ الهجري: {e}")
            self.islamic_date.set("📅 التاريخ الهجري غير متوفر")

    def get_prayer_times(self):
        """حساب أوقات الصلاة"""
        def calculate_times():
            try:
                print("⏰ جاري حساب أوقات الصلاة...")

                # محاولة استخدام API أولاً
                if self.try_api_prayer_times():
                    return

                # حساب محلي كبديل
                self.calculate_local_prayer_times()

            except Exception as e:
                print(f"⚠️ خطأ في حساب أوقات الصلاة: {e}")
                self.use_default_prayer_times()

        threading.Thread(target=calculate_times, daemon=True).start()

    def try_api_prayer_times(self):
        """محاولة الحصول على أوقات الصلاة من API"""
        try:
            city = self.city.get()
            country = self.country.get()
            method = self.settings.get('calculation_method', 4)

            url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method={method}"

            if REQUESTS_AVAILABLE:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data['code'] == 200:
                        self.process_api_prayer_times(data)
                        return True

            # استخدام urllib كبديل
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                if data['code'] == 200:
                    self.process_api_prayer_times(data)
                    return True

        except Exception as e:
            print(f"⚠️ فشل في استخدام API: {e}")

        return False

    def process_api_prayer_times(self, data):
        """معالجة أوقات الصلاة من API"""
        try:
            timings = data['data']['timings']

            # أسماء الصلوات بالعربية
            prayer_names = {
                'Fajr': 'الفجر',
                'Sunrise': 'الشروق',
                'Dhuhr': 'الظهر',
                'Asr': 'العصر',
                'Maghrib': 'المغرب',
                'Isha': 'العشاء'
            }

            self.prayer_times = {}
            for eng_name, ar_name in prayer_names.items():
                if eng_name in timings:
                    time_str = timings[eng_name].split(' ')[0]  # إزالة المنطقة الزمنية
                    self.prayer_times[ar_name] = time_str

            print("✅ تم الحصول على أوقات الصلاة من API")
            self.root.after(0, self.update_prayers_display)
            self.root.after(0, self.update_next_prayer)

        except Exception as e:
            print(f"⚠️ خطأ في معالجة أوقات الصلاة: {e}")
            self.calculate_local_prayer_times()

    def calculate_local_prayer_times(self):
        """حساب أوقات الصلاة محلياً باستخدام الحسابات الفلكية"""
        try:
            print("🔢 حساب أوقات الصلاة محلياً...")

            now = datetime.now()
            lat = self.latitude.get()
            lon = self.longitude.get()

            # حساب اليوم من السنة
            day_of_year = now.timetuple().tm_yday

            # حساب زاوية الشمس
            P = math.asin(0.39795 * math.cos(0.98563 * (day_of_year - 173) * math.pi / 180))

            # حساب معادلة الوقت
            argument = 0.98563 * (day_of_year - 81) * math.pi / 180
            equation_of_time = 4 * (0.000075 + 0.001868 * math.cos(argument) -
                                  0.032077 * math.sin(argument) -
                                  0.014615 * math.cos(2 * argument) -
                                  0.040849 * math.sin(2 * argument))

            # تحويل خط الطول إلى دقائق
            longitude_minutes = lon * 4

            # حساب الأوقات
            lat_rad = lat * math.pi / 180

            # زوايا الصلوات
            fajr_angle = -18  # زاوية الفجر
            isha_angle = -17  # زاوية العشاء

            # حساب الفجر
            fajr_hour_angle = math.acos((-math.sin(fajr_angle * math.pi / 180) -
                                       math.sin(lat_rad) * math.sin(P)) /
                                      (math.cos(lat_rad) * math.cos(P)))
            fajr_time = 12 - (fajr_hour_angle * 180 / math.pi) / 15 - longitude_minutes / 60 + equation_of_time / 60

            # حساب الشروق
            sunrise_hour_angle = math.acos((-math.sin(-0.833 * math.pi / 180) -
                                          math.sin(lat_rad) * math.sin(P)) /
                                         (math.cos(lat_rad) * math.cos(P)))
            sunrise_time = 12 - (sunrise_hour_angle * 180 / math.pi) / 15 - longitude_minutes / 60 + equation_of_time / 60

            # حساب الظهر
            dhuhr_time = 12 - longitude_minutes / 60 + equation_of_time / 60

            # حساب العصر
            asr_hour_angle = math.acos((math.sin(math.atan(1 / (2 + math.tan(abs(lat_rad - P))))) -
                                      math.sin(lat_rad) * math.sin(P)) /
                                     (math.cos(lat_rad) * math.cos(P)))
            asr_time = 12 + (asr_hour_angle * 180 / math.pi) / 15 - longitude_minutes / 60 + equation_of_time / 60

            # حساب المغرب
            maghrib_time = 12 + (sunrise_hour_angle * 180 / math.pi) / 15 - longitude_minutes / 60 + equation_of_time / 60

            # حساب العشاء
            isha_hour_angle = math.acos((-math.sin(isha_angle * math.pi / 180) -
                                       math.sin(lat_rad) * math.sin(P)) /
                                      (math.cos(lat_rad) * math.cos(P)))
            isha_time = 12 + (isha_hour_angle * 180 / math.pi) / 15 - longitude_minutes / 60 + equation_of_time / 60

            # تحويل الأوقات إلى تنسيق 24 ساعة
            def format_time(time_decimal):
                hours = int(time_decimal) % 24
                minutes = int((time_decimal - int(time_decimal)) * 60)
                return f"{hours:02d}:{minutes:02d}"

            self.prayer_times = {
                'الفجر': format_time(fajr_time),
                'الشروق': format_time(sunrise_time),
                'الظهر': format_time(dhuhr_time),
                'العصر': format_time(asr_time),
                'المغرب': format_time(maghrib_time),
                'العشاء': format_time(isha_time)
            }

            print("✅ تم حساب أوقات الصلاة محلياً")
            self.root.after(0, self.update_prayers_display)
            self.root.after(0, self.update_next_prayer)

        except Exception as e:
            print(f"⚠️ خطأ في الحساب المحلي: {e}")
            self.use_default_prayer_times()

    def use_default_prayer_times(self):
        """استخدام أوقات افتراضية للرياض"""
        self.prayer_times = {
            'الفجر': '05:15',
            'الشروق': '06:35',
            'الظهر': '12:10',
            'العصر': '15:25',
            'المغرب': '17:45',
            'العشاء': '19:15'
        }
        print("📍 تم استخدام أوقات الرياض الافتراضية")
        self.root.after(0, self.update_prayers_display)
        self.root.after(0, self.update_next_prayer)

    def update_time(self):
        """تحديث الوقت الحالي"""
        now = datetime.now()
        current_time_str = now.strftime("%H:%M:%S")
        current_date_str = now.strftime("%Y-%m-%d")

        self.current_time.set(f"{current_date_str}\n{current_time_str}")

        # تحديث الصلاة القادمة كل دقيقة
        if now.second == 0:
            self.update_next_prayer()
            self.check_prayer_notifications()

        # جدولة التحديث التالي
        self.root.after(1000, self.update_time)

    def update_next_prayer(self):
        """تحديث معلومات الصلاة القادمة"""
        if not self.prayer_times:
            self.next_prayer.set("⏳ جاري التحميل...")
            self.time_to_next.set("")
            return

        now = datetime.now()
        current_time = now.time()

        # ترتيب الصلوات حسب الوقت (بدون الشروق)
        prayer_order = ['الفجر', 'الظهر', 'العصر', 'المغرب', 'العشاء']

        next_prayer_name = None
        next_prayer_time = None

        for prayer_name in prayer_order:
            if prayer_name in self.prayer_times:
                try:
                    prayer_time_str = self.prayer_times[prayer_name]
                    prayer_time = datetime.strptime(prayer_time_str, "%H:%M").time()

                    if prayer_time > current_time:
                        next_prayer_name = prayer_name
                        next_prayer_time = prayer_time
                        break
                except:
                    continue

        # إذا لم نجد صلاة اليوم، فالصلاة القادمة هي فجر الغد
        if not next_prayer_name and 'الفجر' in self.prayer_times:
            next_prayer_name = 'الفجر (غداً)'
            try:
                next_prayer_time = datetime.strptime(self.prayer_times['الفجر'], "%H:%M").time()
                tomorrow = now + timedelta(days=1)
                next_prayer_datetime = datetime.combine(tomorrow.date(), next_prayer_time)
            except:
                next_prayer_datetime = None
        else:
            next_prayer_datetime = datetime.combine(now.date(), next_prayer_time) if next_prayer_time else None

        if next_prayer_name and next_prayer_datetime:
            time_diff = next_prayer_datetime - now
            hours, remainder = divmod(int(time_diff.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)

            self.next_prayer.set(f"⏰ {next_prayer_name}")
            self.time_to_next.set(f"متبقي: {hours:02d}:{minutes:02d}")
        else:
            self.next_prayer.set("⏰ غير محدد")
            self.time_to_next.set("")

    def check_prayer_notifications(self):
        """فحص وإرسال تنبيهات الصلاة"""
        if not self.notification_enabled.get() or not self.prayer_times:
            return

        now = datetime.now()
        current_time = now.time()

        for prayer_name, prayer_time_str in self.prayer_times.items():
            if prayer_name == 'الشروق':  # تخطي الشروق
                continue

            try:
                prayer_time = datetime.strptime(prayer_time_str, "%H:%M").time()

                # تنبيه وقت الصلاة (مرة واحدة فقط في الدقيقة)
                if (prayer_time.hour == current_time.hour and
                    prayer_time.minute == current_time.minute):
                    self.show_prayer_notification(prayer_name)

            except Exception as e:
                print(f"⚠️ خطأ في فحص التنبيهات: {e}")

    def show_prayer_notification(self, prayer_name):
        """عرض تنبيه الصلاة"""
        try:
            # رسائل تشجيعية متنوعة
            messages = [
                f"🕌 حان الآن وقت صلاة {prayer_name}",
                f"⏰ أذان {prayer_name} - الله أكبر",
                f"🔔 وقت صلاة {prayer_name} قد حان",
                f"📿 صلاة {prayer_name} - بارك الله فيك"
            ]

            message = random.choice(messages)

            # عرض رسالة منبثقة
            messagebox.showinfo(f"🕌 صلاة {prayer_name}", message)

            # تشغيل صوت التنبيه
            if self.sound_enabled.get():
                self.play_notification_sound()

        except Exception as e:
            print(f"⚠️ خطأ في عرض التنبيه: {e}")

    def play_notification_sound(self):
        """تشغيل صوت التنبيه"""
        try:
            if os.name == 'nt':  # Windows
                try:
                    import winsound
                    winsound.MessageBeep(winsound.MB_ICONASTERISK)
                except:
                    pass
            else:  # Linux/Mac
                os.system('echo -e "\\a"')
        except Exception as e:
            print(f"⚠️ لا يمكن تشغيل الصوت: {e}")

    def mark_prayer_completed(self, prayer_name):
        """تسجيل إتمام صلاة"""
        if self.prayers_completed_today < 5:
            self.prayers_completed_today += 1
            self.total_prayers_month += 1
            self.update_prayer_counter()
            self.save_prayer_statistics()

            # رسائل تشجيعية
            encouragement_messages = [
                f"✅ بارك الله فيك! تم تسجيل صلاة {prayer_name}",
                f"🌟 أحسنت! صلاة {prayer_name} مكتملة",
                f"✨ جزاك الله خيراً! {prayer_name} ✓",
                f"🎉 ممتاز! تم تسجيل {prayer_name} بنجاح"
            ]

            message = random.choice(encouragement_messages)
            messagebox.showinfo("تم التسجيل", message)
        else:
            messagebox.showinfo("مكتمل", "تم تسجيل جميع صلوات اليوم! 🎉")

    def schedule_updates(self):
        """جدولة التحديثات الدورية"""
        # تحديث كل 5 دقائق
        self.root.after(300000, self.schedule_updates)

        now = datetime.now()

        # تحديث التاريخ الهجري يومياً في منتصف الليل
        if now.hour == 0 and now.minute == 0:
            self.get_islamic_date()
            # إعادة تعيين عداد الصلوات
            self.prayers_completed_today = 0
            self.update_prayer_counter()
            self.save_prayer_statistics()

        # تحديث الطقس كل ساعة
        if now.minute == 0:
            if self.settings.get('show_weather', True):
                self.get_weather_info()

    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        # إنشاء إطار رئيسي قابل للتمرير
        main_canvas = tk.Canvas(self.root, bg='#0f172a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg='#0f172a')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # العنوان الرئيسي
        self.create_header(scrollable_frame)

        # معلومات الموقع والطقس
        self.create_info_section(scrollable_frame)

        # معلومات إضافية (القبلة والتاريخ الهجري)
        self.create_extra_info_section(scrollable_frame)

        # إحصائيات الصلاة
        self.create_stats_section(scrollable_frame)

        # أزرار التحكم
        self.create_control_buttons(scrollable_frame)

        # عرض الوقت الحالي
        self.create_time_section(scrollable_frame)

        # الصلاة القادمة
        self.create_next_prayer_section(scrollable_frame)

        # جدول أوقات الصلاة
        self.create_prayers_section(scrollable_frame)

        # الروابط والمساعدة
        self.create_footer_section(scrollable_frame)

        # حفظ مرجع للإطار
        self.scrollable_frame = scrollable_frame

    def create_header(self, parent):
        """إنشاء العنوان الرئيسي"""
        header_frame = tk.Frame(parent, bg='#1e293b', relief='raised', bd=3)
        header_frame.pack(fill='x', padx=10, pady=10)

        title_label = tk.Label(
            header_frame,
            text="🕌 أوقات الصلاة المتقدم 🕌",
            font=("Arial", 24, "bold"),
            bg='#1e293b',
            fg='#f1f5f9'
        )
        title_label.pack(pady=15)

        subtitle_label = tk.Label(
            header_frame,
            text="Advanced Prayer Times Application v2.0",
            font=("Arial", 12, "italic"),
            bg='#1e293b',
            fg='#94a3b8'
        )
        subtitle_label.pack(pady=(0, 10))

    def create_info_section(self, parent):
        """إنشاء قسم معلومات الموقع والطقس"""
        info_frame = tk.Frame(parent, bg='#0f172a')
        info_frame.pack(fill='x', padx=10, pady=5)

        # إطار الموقع
        location_frame = tk.Frame(info_frame, bg='#334155', relief='raised', bd=2)
        location_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        tk.Label(
            location_frame,
            text="📍 الموقع الحالي",
            font=("Arial", 12, "bold"),
            bg='#334155',
            fg='#f1f5f9'
        ).pack(pady=5)

        tk.Label(
            location_frame,
            textvariable=self.location_info,
            font=("Arial", 10),
            bg='#334155',
            fg='#cbd5e1',
            wraplength=200
        ).pack(pady=(0, 10))

        # إطار الطقس
        weather_frame = tk.Frame(info_frame, bg='#1e40af', relief='raised', bd=2)
        weather_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        tk.Label(
            weather_frame,
            text="🌤️ حالة الطقس",
            font=("Arial", 12, "bold"),
            bg='#1e40af',
            fg='white'
        ).pack(pady=5)

        tk.Label(
            weather_frame,
            textvariable=self.weather_info,
            font=("Arial", 10),
            bg='#1e40af',
            fg='#dbeafe',
            wraplength=200
        ).pack(pady=(0, 10))

    def create_extra_info_section(self, parent):
        """إنشاء قسم المعلومات الإضافية"""
        extra_frame = tk.Frame(parent, bg='#0f172a')
        extra_frame.pack(fill='x', padx=10, pady=5)

        # إطار اتجاه القبلة
        qibla_frame = tk.Frame(extra_frame, bg='#065f46', relief='raised', bd=2)
        qibla_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        tk.Label(
            qibla_frame,
            text="🧭 اتجاه القبلة",
            font=("Arial", 12, "bold"),
            bg='#065f46',
            fg='white'
        ).pack(pady=5)

        tk.Label(
            qibla_frame,
            textvariable=self.qibla_direction,
            font=("Arial", 10),
            bg='#065f46',
            fg='#d1fae5',
            wraplength=200
        ).pack(pady=(0, 10))

        # إطار التاريخ الهجري
        hijri_frame = tk.Frame(extra_frame, bg='#7c2d12', relief='raised', bd=2)
        hijri_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        tk.Label(
            hijri_frame,
            text="📅 التاريخ الهجري",
            font=("Arial", 12, "bold"),
            bg='#7c2d12',
            fg='white'
        ).pack(pady=5)

        tk.Label(
            hijri_frame,
            textvariable=self.islamic_date,
            font=("Arial", 10),
            bg='#7c2d12',
            fg='#fed7aa',
            wraplength=200
        ).pack(pady=(0, 10))

    def create_stats_section(self, parent):
        """إنشاء قسم الإحصائيات"""
        stats_frame = tk.Frame(parent, bg='#581c87', relief='raised', bd=2)
        stats_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(
            stats_frame,
            text="📊 إحصائيات الصلاة",
            font=("Arial", 12, "bold"),
            bg='#581c87',
            fg='white'
        ).pack(pady=5)

        tk.Label(
            stats_frame,
            textvariable=self.prayer_counter,
            font=("Arial", 11, "bold"),
            bg='#581c87',
            fg='#e9d5ff'
        ).pack(pady=(0, 10))

    def create_control_buttons(self, parent):
        """إنشاء أزرار التحكم"""
        control_frame = tk.Frame(parent, bg='#475569', relief='raised', bd=2)
        control_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(
            control_frame,
            text="🎛️ أزرار التحكم",
            font=("Arial", 12, "bold"),
            bg='#475569',
            fg='white'
        ).pack(pady=5)

        buttons_frame = tk.Frame(control_frame, bg='#475569')
        buttons_frame.pack(pady=10)

        # أزرار التحكم
        buttons = [
            ("🔄 تحديث الأوقات", self.get_prayer_times, '#059669'),
            ("📍 تحديد موقعي", self.detect_location, '#dc2626'),
            ("⚙️ الإعدادات", self.show_settings, '#7c3aed'),
            ("ℹ️ حول التطبيق", self.show_about, '#1e40af')
        ]

        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                font=("Arial", 10, "bold"),
                bg=color,
                fg='white',
                cursor='hand2',
                relief='raised',
                bd=2,
                width=15
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=5)

    def create_time_section(self, parent):
        """إنشاء قسم الوقت الحالي"""
        time_frame = tk.Frame(parent, bg='#1e40af', relief='raised', bd=3)
        time_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(
            time_frame,
            text="🕐 الوقت الحالي",
            font=("Arial", 16, "bold"),
            bg='#1e40af',
            fg='white'
        ).pack(pady=10)

        tk.Label(
            time_frame,
            textvariable=self.current_time,
            font=("Arial", 20, "bold"),
            bg='#1e40af',
            fg='#fbbf24'
        ).pack(pady=10)

    def create_next_prayer_section(self, parent):
        """إنشاء قسم الصلاة القادمة"""
        next_frame = tk.Frame(parent, bg='#059669', relief='raised', bd=3)
        next_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(
            next_frame,
            text="⏰ الصلاة القادمة",
            font=("Arial", 14, "bold"),
            bg='#059669',
            fg='white'
        ).pack(pady=5)

        tk.Label(
            next_frame,
            textvariable=self.next_prayer,
            font=("Arial", 18, "bold"),
            bg='#059669',
            fg='white'
        ).pack(pady=5)

        tk.Label(
            next_frame,
            textvariable=self.time_to_next,
            font=("Arial", 14),
            bg='#059669',
            fg='#d1fae5'
        ).pack(pady=(0, 10))

    def create_prayers_section(self, parent):
        """إنشاء قسم جدول أوقات الصلاة"""
        prayers_main_frame = tk.Frame(parent, bg='#0f172a')
        prayers_main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        tk.Label(
            prayers_main_frame,
            text="📋 جدول أوقات الصلاة اليوم",
            font=("Arial", 18, "bold"),
            bg='#0f172a',
            fg='#f1f5f9'
        ).pack(pady=10)

        # إطار الصلوات
        self.prayers_frame = tk.Frame(prayers_main_frame, bg='#0f172a')
        self.prayers_frame.pack(fill='both', expand=True, padx=10)

    def create_footer_section(self, parent):
        """إنشاء قسم الروابط والمساعدة"""
        footer_frame = tk.Frame(parent, bg='#1f2937', relief='raised', bd=2)
        footer_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(
            footer_frame,
            text="🔗 روابط مفيدة",
            font=("Arial", 12, "bold"),
            bg='#1f2937',
            fg='white'
        ).pack(pady=5)

        links_frame = tk.Frame(footer_frame, bg='#1f2937')
        links_frame.pack(pady=5)

        # روابط مفيدة
        links = [
            ("🌐 موقع الحرمين", "https://www.haramain.sa"),
            ("📱 تطبيق الأذان", "https://play.google.com/store/apps/details?id=com.athan"),
            ("📖 القرآن الكريم", "https://quran.com")
        ]

        for text, url in links:
            btn = tk.Button(
                links_frame,
                text=text,
                command=lambda u=url: webbrowser.open(u),
                font=("Arial", 9),
                bg='#065f46',
                fg='white',
                cursor='hand2'
            )
            btn.pack(side='left', padx=5)

    def update_prayers_display(self):
        """تحديث عرض أوقات الصلاة"""
        # مسح العرض السابق
        for widget in self.prayers_frame.winfo_children():
            widget.destroy()

        if not self.prayer_times:
            no_data_label = tk.Label(
                self.prayers_frame,
                text="⏳ جاري تحميل أوقات الصلاة...",
                font=("Arial", 14),
                bg='#0f172a',
                fg='#94a3b8'
            )
            no_data_label.pack(pady=20)
            return

        # إنشاء بطاقة لكل صلاة
        for prayer_name, prayer_time in self.prayer_times.items():
            self.create_prayer_card(prayer_name, prayer_time)

    def create_prayer_card(self, prayer_name, prayer_time):
        """إنشاء بطاقة صلاة"""
        # إطار البطاقة
        card_frame = tk.Frame(
            self.prayers_frame,
            bg=self.prayer_colors.get(prayer_name, '#374151'),
            relief='raised',
            bd=3
        )
        card_frame.pack(fill='x', pady=5, padx=5)

        # محتوى البطاقة
        content_frame = tk.Frame(card_frame, bg=self.prayer_colors.get(prayer_name, '#374151'))
        content_frame.pack(fill='x', padx=15, pady=10)

        # الجانب الأيسر (الأيقونة والاسم)
        left_frame = tk.Frame(content_frame, bg=self.prayer_colors.get(prayer_name, '#374151'))
        left_frame.pack(side='left', fill='y')

        # الأيقونة
        icon_label = tk.Label(
            left_frame,
            text=self.prayer_icons.get(prayer_name, '🕌'),
            font=("Arial", 24),
            bg=self.prayer_colors.get(prayer_name, '#374151')
        )
        icon_label.pack(side='left', padx=(0, 10))

        # اسم الصلاة
        name_label = tk.Label(
            left_frame,
            text=prayer_name,
            font=("Arial", 16, "bold"),
            bg=self.prayer_colors.get(prayer_name, '#374151'),
            fg='white'
        )
        name_label.pack(side='left', anchor='w')

        # الجانب الأيمن (الوقت والزر)
        right_frame = tk.Frame(content_frame, bg=self.prayer_colors.get(prayer_name, '#374151'))
        right_frame.pack(side='right', anchor='e')

        # وقت الصلاة
        time_label = tk.Label(
            right_frame,
            text=prayer_time,
            font=("Arial", 18, "bold"),
            bg=self.prayer_colors.get(prayer_name, '#374151'),
            fg='#fbbf24'
        )
        time_label.pack(side='top')

        # زر تسجيل الصلاة (فقط للصلوات وليس الشروق)
        if prayer_name != 'الشروق':
            mark_btn = tk.Button(
                right_frame,
                text="✅ تم",
                command=lambda p=prayer_name: self.mark_prayer_completed(p),
                font=("Arial", 8, "bold"),
                bg='#059669',
                fg='white',
                cursor='hand2',
                relief='raised',
                bd=1,
                width=6
            )
            mark_btn.pack(side='bottom', pady=(5, 0))

    def show_settings(self):
        """عرض نافذة الإعدادات"""
        messagebox.showinfo("الإعدادات", "نافذة الإعدادات ستكون متوفرة قريباً!")

    def show_about(self):
        """عرض معلومات التطبيق"""
        about_text = """
🕌 تطبيق أوقات الصلاة المتقدم 🕌
Advanced Prayer Times Application

الإصدار: 2.0
المطور: مساعد الذكي المتقدم

المميزات:
✅ تحديد الموقع تلقائياً
✅ عرض حالة الطقس الحية
✅ حساب اتجاه القبلة
✅ التاريخ الهجري
✅ إحصائيات الصلاة
✅ تنبيهات ذكية
✅ تصميم حديث وجذاب
✅ واجهة عربية كاملة

المكتبات المستخدمة:
• tkinter - واجهة المستخدم
• requests - الاتصال بالإنترنت (اختيارية)
• urllib - بديل requests (مدمج)
• json - معالجة البيانات
• threading - العمليات المتوازية
• datetime - التاريخ والوقت
• math - الحسابات الفلكية

🕌 بارك الله فيكم 🕌
        """
        messagebox.showinfo("حول التطبيق", about_text)

def main():
    """الدالة الرئيسية لتشغيل التطبيق"""
    try:
        print("🚀 بدء تشغيل تطبيق أوقات الصلاة المتقدم...")

        # إنشاء النافذة الرئيسية
        root = tk.Tk()

        # إنشاء التطبيق
        app = PrayerTimesApp(root)

        print("✅ تم تشغيل التطبيق بنجاح!")

        # تشغيل حلقة الأحداث
        root.mainloop()

    except KeyboardInterrupt:
        print("⏹️ تم إغلاق التطبيق بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ في تشغيل التطبيق: {e}")
        messagebox.showerror("خطأ", f"حدث خطأ في تشغيل التطبيق:\n{e}")

if __name__ == "__main__":
    main()
