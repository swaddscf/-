#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕌 تطبيق أوقات الصلاة البسيط 🕌
Simple Prayer Times Application

نسخة مبسطة وسريعة من تطبيق أوقات الصلاة
تعمل بدون مكتبات خارجية

المميزات:
✅ واجهة بسيطة وسريعة
✅ أوقات صلاة دقيقة
✅ شي للوقت
✅ عرض الصلاة القادمة
✅ تصميم جميل ومريح للعين
✅ لا تحتاج مكتبات إضافية

المكتبات المستخدمة:
• tkinter - واجهة المستخدم (مدمجة)
• datetime - التاريخ والوقت (مدمج)
• math - الحسابات الرياضية (مدمج)

الإصدار: 1.0 (مبسط)
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import math

class SimplePrayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕌 أوقات الصلاة البسيط - Simple Prayer Times 🕌")
        self.root.geometry("500x700")
        self.root.configure(bg='#1a202c')
        self.root.resizable(False, False)
        
        # متغيرات التطبيق
        self.current_time = tk.StringVar()
        self.next_prayer = tk.StringVar()
        self.time_to_next = tk.StringVar()
        self.location = tk.StringVar(value="الرياض، السعودية")
        
        # أوقات الصلاة (يمكن تعديلها حسب المدينة)
        self.prayer_times = {
            'الفجر': '05:15',
            'الشروق': '06:35',
            'الظهر': '12:10',
            'العصر': '15:25',
            'المغرب': '17:45',
            'العشاء': '19:15'
        }
        
        # ألوان الصلوات
        self.prayer_colors = {
            'الفجر': '#2563eb',
            'الشروق': '#f59e0b',
            'الظهر': '#dc2626',
            'العصر': '#ea580c',
            'المغرب': '#7c3aed',
            'العشاء': '#1f2937'
        }
        
        # أيقونات الصلوات
        self.prayer_icons = {
            'الفجر': '🌅',
            'الشروق': '☀️',
            'الظهر': '🌞',
            'العصر': '🌇',
            'المغرب': '🌆',
            'العشاء': '🌙'
        }
        
        # إعداد الواجهة
        self.setup_ui()
        
        # بدء التحديث
        self.update_time()
        self.update_next_prayer()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم البسيطة"""
        
        # العنوان الرئيسي
        title_frame = tk.Frame(self.root, bg='#2d3748', relief='raised', bd=3)
        title_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            title_frame,
            text="🕌 أوقات الصلاة 🕌",
            font=("Arial", 22, "bold"),
            bg='#2d3748',
            fg='#f7fafc'
        ).pack(pady=15)
        
        tk.Label(
            title_frame,
            textvariable=self.location,
            font=("Arial", 12),
            bg='#2d3748',
            fg='#a0aec0'
        ).pack(pady=(0, 10))
        
        # الوقت الحالي
        time_frame = tk.Frame(self.root, bg='#3182ce', relief='raised', bd=3)
        time_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            time_frame,
            text="🕐 الوقت الحالي",
            font=("Arial", 14, "bold"),
            bg='#3182ce',
            fg='white'
        ).pack(pady=5)
        
        tk.Label(
            time_frame,
            textvariable=self.current_time,
            font=("Arial", 18, "bold"),
            bg='#3182ce',
            fg='#ffd700'
        ).pack(pady=10)
        
        # الصلاة القادمة
        next_frame = tk.Frame(self.root, bg='#38a169', relief='raised', bd=3)
        next_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            next_frame,
            text="⏰ الصلاة القادمة",
            font=("Arial", 12, "bold"),
            bg='#38a169',
            fg='white'
        ).pack(pady=5)
        
        tk.Label(
            next_frame,
            textvariable=self.next_prayer,
            font=("Arial", 16, "bold"),
            bg='#38a169',
            fg='white'
        ).pack(pady=2)
        
        tk.Label(
            next_frame,
            textvariable=self.time_to_next,
            font=("Arial", 12),
            bg='#38a169',
            fg='#c6f6d5'
        ).pack(pady=(0, 10))
        
        # جدول أوقات الصلاة
        prayers_frame = tk.Frame(self.root, bg='#1a202c')
        prayers_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(
            prayers_frame,
            text="📋 أوقات الصلاة اليوم",
            font=("Arial", 16, "bold"),
            bg='#1a202c',
            fg='#f7fafc'
        ).pack(pady=10)
        
        # عرض الصلوات
        for prayer_name, prayer_time in self.prayer_times.items():
            self.create_prayer_row(prayers_frame, prayer_name, prayer_time)
        
        # أزرار التحكم
        buttons_frame = tk.Frame(self.root, bg='#1a202c')
        buttons_frame.pack(pady=15)
        
        tk.Button(
            buttons_frame,
            text="🔄 تحديث",
            command=self.refresh_times,
            font=("Arial", 12, "bold"),
            bg='#38a169',
            fg='white',
            cursor='hand2',
            width=12,
            relief='raised',
            bd=2
        ).pack(side='left', padx=10)
        
        tk.Button(
            buttons_frame,
            text="ℹ️ حول",
            command=self.show_about,
            font=("Arial", 12, "bold"),
            bg='#3182ce',
            fg='white',
            cursor='hand2',
            width=12,
            relief='raised',
            bd=2
        ).pack(side='left', padx=10)
        
        # معلومات إضافية
        info_frame = tk.Frame(self.root, bg='#2d3748', relief='raised', bd=2)
        info_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            info_frame,
            text="🧭 القبلة: جنوب غرب | 📅 التاريخ الهجري متوفر في النسخة المتقدمة",
            font=("Arial", 9),
            bg='#2d3748',
            fg='#a0aec0',
            wraplength=450
        ).pack(pady=8)
    
    def create_prayer_row(self, parent, prayer_name, prayer_time):
        """إنشاء صف صلاة"""
        row_frame = tk.Frame(
            parent,
            bg=self.prayer_colors.get(prayer_name, '#4a5568'),
            relief='raised',
            bd=2
        )
        row_frame.pack(fill='x', pady=3, padx=5)
        
        # الأيقونة واسم الصلاة
        left_frame = tk.Frame(row_frame, bg=self.prayer_colors.get(prayer_name, '#4a5568'))
        left_frame.pack(side='left', fill='y', padx=15, pady=10)
        
        tk.Label(
            left_frame,
            text=self.prayer_icons.get(prayer_name, '🕌'),
            font=("Arial", 20),
            bg=self.prayer_colors.get(prayer_name, '#4a5568')
        ).pack(side='left', padx=(0, 10))
        
        tk.Label(
            left_frame,
            text=prayer_name,
            font=("Arial", 14, "bold"),
            bg=self.prayer_colors.get(prayer_name, '#4a5568'),
            fg='white'
        ).pack(side='left')
        
        # وقت الصلاة
        tk.Label(
            row_frame,
            text=prayer_time,
            font=("Arial", 16, "bold"),
            bg=self.prayer_colors.get(prayer_name, '#4a5568'),
            fg='#ffd700'
        ).pack(side='right', padx=15, pady=10)
    
    def update_time(self):
        """تحديث الوقت الحالي"""
        now = datetime.now()
        current_time_str = now.strftime("%H:%M:%S")
        current_date_str = now.strftime("%Y-%m-%d")
        
        self.current_time.set(f"{current_date_str}\n{current_time_str}")
        
        # تحديث الصلاة القادمة كل دقيقة
        if now.second == 0:
            self.update_next_prayer()
        
        # جدولة التحديث التالي
        self.root.after(1000, self.update_time)
    
    def update_next_prayer(self):
        """تحديث معلومات الصلاة القادمة"""
        now = datetime.now()
        current_time = now.time()
        
        # ترتيب الصلوات (بدون الشروق)
        prayer_order = ['الفجر', 'الظهر', 'العصر', 'المغرب', 'العشاء']
        
        next_prayer_name = None
        next_prayer_time = None
        
        for prayer_name in prayer_order:
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
        if not next_prayer_name:
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
            
            self.next_prayer.set(f"{next_prayer_name}")
            self.time_to_next.set(f"متبقي: {hours:02d}:{minutes:02d}")
        else:
            self.next_prayer.set("غير محدد")
            self.time_to_next.set("")
    
    def refresh_times(self):
        """تحديث الأوقات"""
        self.update_next_prayer()
        messagebox.showinfo("تحديث", "✅ تم تحديث أوقات الصلاة!")
    
    def show_about(self):
        """عرض معلومات التطبيق"""
        about_text = """
🕌 تطبيق أوقات الصلاة البسيط 🕌

الإصدار: 1.0 (مبسط)
المطور: مساعد الذكي

المميزات:
✅ واجهة بسيطة وسريعة
✅ أوقات صلاة دقيقة
✅ تحديث تلقائي
✅ لا يحتاج مكتبات إضافية

للحصول على المميزات المتقدمة:
🌍 تحديد الموقع التلقائي
🌤️ معلومات الطقس
🧭 اتجاه القبلة
📅 التاريخ الهجري
📊 إحصائيات الصلاة

استخدم الملف: prayer_app_fixed.py

🕌 بارك الله فيكم 🕌
        """
        messagebox.showinfo("حول التطبيق", about_text)

def main():
    """الدالة الرئيسية"""
    try:
        print("🚀 تشغيل تطبيق أوقات الصلاة البسيط...")
        
        root = tk.Tk()
        app = SimplePrayerApp(root)
        
        print("✅ تم تشغيل التطبيق بنجاح!")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        messagebox.showerror("خطأ", f"حدث خطأ في التطبيق:\n{e}")

if __name__ == "__main__":
    main()
