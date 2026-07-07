#!/usr/bin/env python3
"""Normalize Telegram export JSON into an inspectable intermediate dataset."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CATEGORY_KEYWORDS = {
    "Onboarding": (
        "onboarding",
        "setup",
        "install",
        "access",
        "guide",
        "environment",
        "how to start",
        "онбординг",
        "настро",
        "установ",
        "доступ",
        "как начать",
        "с чего начать",
        "підключ",
        "configurar",
        "instalar",
        "acceso",
        "ambiente",
        "guía",
        "guia",
        "configurar",
        "instalar",
        "acesso",
        "ambiente",
        "guide",
        "installer",
        "accès",
        "umgebung",
        "einrichten",
        "zugang",
        "konfiguracja",
        "instalacja",
        "dostęp",
        "kurulum",
        "erişim",
        "إعداد",
        "تثبيت",
        "وصول",
        "सेटअप",
        "इंस्टॉल",
        "akses",
        "instal",
        "cài đặt",
        "truy cập",
    ),
    "Backend": (
        "backend",
        "server",
        "api",
        "endpoint",
        "database",
        "sql",
        "migration",
        "auth",
        "бекенд",
        "бэкенд",
        "сервер",
        "эндпоинт",
        "ендпоінт",
        "база",
        "запрос",
        "запит",
        "авториза",
        "логин",
        "servidor",
        "base de datos",
        "autenticación",
        "autenticacao",
        "banco de dados",
        "serveur",
        "base de données",
        "authentification",
        "datenbank",
        "anmeldung",
        "uwierzyteln",
        "baza danych",
        "sunucu",
        "veritaban",
        "kimlik doğrulama",
        "خادم",
        "قاعدة بيانات",
        "مصادقة",
        "सर्वर",
        "डेटाबेस",
        "प्रमाणीकरण",
        "basis data",
        "otentikasi",
        "máy chủ",
        "cơ sở dữ liệu",
        "xác thực",
    ),
    "Business Logic": (
        "business",
        "rule",
        "logic",
        "pricing",
        "invoice",
        "payment",
        "subscription",
        "flow",
        "бизнес",
        "бізнес",
        "правил",
        "логик",
        "оплат",
        "бронь",
        "броню",
        "билет",
        "клиент",
        "баланс",
        "зал",
        "negocio",
        "regla",
        "pago",
        "suscripción",
        "cliente",
        "reserva",
        "negócio",
        "regra",
        "pagamento",
        "assinatura",
        "cliente",
        "reserva",
        "métier",
        "règle",
        "paiement",
        "abonnement",
        "client",
        "buchung",
        "zahlung",
        "kunde",
        "geschäft",
        "reguła",
        "płatność",
        "klient",
        "rezerwacja",
        "ödeme",
        "müşteri",
        "rezervasyon",
        "اشتراك",
        "دفع",
        "عميل",
        "حجز",
        "भुगतान",
        "ग्राहक",
        "नियम",
        "pembayaran",
        "pelanggan",
        "langganan",
        "quy tắc",
        "thanh toán",
        "khách hàng",
        "đặt chỗ",
    ),
    "Mobile": (
        "android",
        "ios",
        "mobile",
        "compose",
        "swift",
        "kotlin",
        "app",
        "build",
        "screen",
        "мобил",
        "мобіль",
        "приложени",
        "застосунк",
        "экран",
        "екран",
        "compose",
        "swiftui",
        "móvil",
        "movil",
        "aplicación",
        "pantalla",
        "móvel",
        "aplicativo",
        "tela",
        "écran",
        "mobile",
        "anwendung",
        "bildschirm",
        "mobilna",
        "aplikacja",
        "ekran",
        "uygulama",
        "mobil",
        "ekran",
        "تطبيق",
        "هاتف",
        "شاشة",
        "ऐप",
        "मोबाइल",
        "स्क्रीन",
        "aplikasi",
        "layar",
        "ứng dụng",
        "di động",
        "màn hình",
    ),
    "UI": (
        "ui",
        "ux",
        "design",
        "layout",
        "button",
        "modal",
        "color",
        "font",
        "spacing",
        "дизайн",
        "фигма",
        "figma",
        "иконк",
        "кнопк",
        "цвет",
        "колір",
        "шрифт",
        "стил",
        "локализа",
        "diseño",
        "botón",
        "color",
        "fuente",
        "diseño",
        "botão",
        "cor",
        "fonte",
        "conception",
        "bouton",
        "couleur",
        "police",
        "entwurf",
        "schaltfläche",
        "farbe",
        "schrift",
        "projekt",
        "przycisk",
        "kolor",
        "czcionka",
        "tasarım",
        "düğme",
        "renk",
        "yazı tipi",
        "تصميم",
        "زر",
        "لون",
        "خط",
        "डिजाइन",
        "बटन",
        "रंग",
        "desain",
        "tombol",
        "warna",
        "thiết kế",
        "nút",
        "màu",
    ),
    "Security Notes": (
        "security",
        "token",
        "secret",
        "permission",
        "credential",
        "privacy",
        "encrypt",
        "2fa",
        "безопас",
        "безпек",
        "токен",
        "секрет",
        "ключ",
        "шифр",
        "приват",
        "seguridad",
        "permiso",
        "credencial",
        "privacidad",
        "segurança",
        "permissão",
        "credencial",
        "privacidade",
        "sécurité",
        "autorisation",
        "identifiant",
        "confidentialité",
        "sicherheit",
        "berechtigung",
        "datenschutz",
        "bezpieczeństwo",
        "uprawnienie",
        "poświadczenie",
        "güvenlik",
        "izin",
        "kimlik bilgisi",
        "gizlilik",
        "أمان",
        "صلاحية",
        "اعتماد",
        "خصوصية",
        "सुरक्षा",
        "अनुमति",
        "क्रेडेंशियल",
        "keamanan",
        "izin",
        "privasi",
        "bảo mật",
        "quyền",
        "riêng tư",
    ),
    "API Reference": (
        "request",
        "response",
        "payload",
        "header",
        "status code",
        "schema",
        "field",
        "contract",
        "реквест",
        "response",
        "ответ",
        "відповідь",
        "поле",
        "схема",
        "контракт",
        "хедер",
        "заголов",
        "solicitud",
        "respuesta",
        "campo",
        "esquema",
        "contrato",
        "requisição",
        "resposta",
        "campo",
        "contrato",
        "requête",
        "réponse",
        "champ",
        "schéma",
        "anforderung",
        "antwort",
        "feld",
        "schema",
        "żądanie",
        "odpowiedź",
        "pole",
        "schemat",
        "istek",
        "yanıt",
        "alan",
        "şema",
        "طلب",
        "استجابة",
        "حقل",
        "مخطط",
        "अनुरोध",
        "जवाब",
        "फ़ील्ड",
        "स्कीमा",
        "permintaan",
        "respons",
        "kolom",
        "skema",
        "yêu cầu",
        "phản hồi",
        "trường",
        "lược đồ",
    ),
    "Solved Issues": (
        "fixed",
        "resolved",
        "works now",
        "done",
        "solved",
        "patch",
        "merged",
        "исправ",
        "виправ",
        "почини",
        "пофикс",
        "готово",
        "решили",
        "зробили",
        "arreglado",
        "resuelto",
        "corregido",
        "hecho",
        "corrigido",
        "resolvido",
        "feito",
        "corrigé",
        "résolu",
        "terminé",
        "behoben",
        "gelöst",
        "erledigt",
        "naprawione",
        "rozwiązane",
        "zrobione",
        "düzeltildi",
        "çözüldü",
        "tamamlandı",
        "تم الإصلاح",
        "تم الحل",
        "पूर्ण",
        "हल",
        "ठीक",
        "diperbaiki",
        "selesai",
        "đã sửa",
        "đã giải quyết",
        "hoàn thành",
    ),
    "Known Problems": (
        "bug",
        "issue",
        "problem",
        "broken",
        "fails",
        "error",
        "crash",
        "regression",
        "баг",
        "ошиб",
        "помил",
        "проблем",
        "падает",
        "падає",
        "не работает",
        "не працює",
        "регресс",
        "error",
        "fallo",
        "problema",
        "roto",
        "falha",
        "problema",
        "quebrado",
        "erreur",
        "problème",
        "cassé",
        "fehler",
        "problem",
        "kaputt",
        "błąd",
        "problem",
        "zepsute",
        "hata",
        "sorun",
        "bozuk",
        "خطأ",
        "مشكلة",
        "معطل",
        "त्रुटि",
        "समस्या",
        "rusak",
        "masalah",
        "lỗi",
        "sự cố",
        "hỏng",
    ),
}

TYPE_KEYWORDS = {
    "decision": (
        "decide",
        "decision",
        "agreed",
        "we will",
        "let's do",
        "final",
        "решили",
        "договорились",
        "итог",
        "финально",
        "робимо",
        "вирішили",
        "decidido",
        "acordado",
        "final",
        "decidido",
        "combinado",
        "final",
        "décidé",
        "accord",
        "final",
        "entschieden",
        "vereinbart",
        "final",
        "ustalone",
        "decyzja",
        "finalnie",
        "karar",
        "anlaştık",
        "nihai",
        "قررنا",
        "اتفقنا",
        "نهائي",
        "निर्णय",
        "तय",
        "अंतिम",
        "diputuskan",
        "sepakat",
        "final",
        "quyết định",
        "thống nhất",
        "cuối cùng",
    ),
    "issue": (
        "bug",
        "issue",
        "error",
        "broken",
        "crash",
        "problem",
        "fails",
        "баг",
        "ошиб",
        "помил",
        "сломал",
        "не работает",
        "не працює",
        "fallo",
        "problema",
        "roto",
        "falha",
        "quebrado",
        "erreur",
        "problème",
        "cassé",
        "fehler",
        "kaputt",
        "błąd",
        "zepsute",
        "hata",
        "sorun",
        "خطأ",
        "مشكلة",
        "त्रुटि",
        "समस्या",
        "masalah",
        "rusak",
        "lỗi",
        "sự cố",
    ),
    "question_answer": (
        "?",
        "how",
        "why",
        "what",
        "where",
        "can we",
        "should we",
        "как",
        "почему",
        "зачем",
        "что",
        "где",
        "можем",
        "можно",
        "чому",
        "навіщо",
        "cómo",
        "por qué",
        "qué",
        "dónde",
        "como",
        "por que",
        "o que",
        "onde",
        "comment",
        "pourquoi",
        "quoi",
        "où",
        "wie",
        "warum",
        "was",
        "wo",
        "jak",
        "dlaczego",
        "co",
        "gdzie",
        "nasıl",
        "neden",
        "ne",
        "nerede",
        "كيف",
        "لماذا",
        "ماذا",
        "أين",
        "कैसे",
        "क्यों",
        "क्या",
        "कहाँ",
        "bagaimana",
        "mengapa",
        "apa",
        "di mana",
        "như thế nào",
        "tại sao",
        "cái gì",
        "ở đâu",
    ),
    "task": (
        "todo",
        "task",
        "need to",
        "please",
        "follow up",
        "next step",
        "надо",
        "нужно",
        "треба",
        "сделать",
        "зробити",
        "запинить",
        "добавить",
        "додати",
        "hacer",
        "agregar",
        "necesario",
        "tarea",
        "fazer",
        "adicionar",
        "precisa",
        "tarefa",
        "faire",
        "ajouter",
        "nécessaire",
        "tâche",
        "machen",
        "hinzufügen",
        "notwendig",
        "aufgabe",
        "zrobić",
        "dodać",
        "trzeba",
        "zadanie",
        "yap",
        "ekle",
        "gerek",
        "görev",
        "افعل",
        "أضف",
        "مطلوب",
        "कार्य",
        "करना",
        "जोड़",
        "perlu",
        "tambahkan",
        "tugas",
        "cần",
        "thêm",
        "nhiệm vụ",
    ),
    "reference": (
        "doc",
        "docs",
        "link",
        "spec",
        "figma",
        "ticket",
        "notion",
        "ссылка",
        "посилання",
        "док",
        "дока",
        "докум",
        "фигма",
        "макет",
        "enlace",
        "documento",
        "especificación",
        "billete",
        "link",
        "documento",
        "especificação",
        "chamado",
        "lien",
        "document",
        "spécification",
        "ticket",
        "link",
        "dokument",
        "spezifikation",
        "ticket",
        "link",
        "dokument",
        "specyfikacja",
        "zgłoszenie",
        "bağlantı",
        "belge",
        "şartname",
        "bilet",
        "رابط",
        "مستند",
        "مواصفة",
        "تذكرة",
        "लिंक",
        "दस्तावेज़",
        "स्पेक",
        "tautan",
        "dokumen",
        "spesifikasi",
        "tiket",
        "liên kết",
        "tài liệu",
        "đặc tả",
        "vé",
    ),
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "has",
    "have",
    "if",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "we",
    "with",
    "you",
}

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\w)(\+?\d[\d(). -]{7,}\d)(?!\w)")
TOKEN_RE = re.compile(r"\b[a-zA-Z0-9_\-]{24,}\b")
URL_RE = re.compile(r"https?://\S+")
MESSAGE_ID_RE = re.compile(r"\bmessage(?:_id)?\s*[:=]?\s*\d+\b", re.IGNORECASE)
WORD_RE = re.compile(r"[^\W\d_][^\W_]{2,}", re.UNICODE)


@dataclass
class RedactionStats:
    emails: int = 0
    phones: int = 0
    tokens: int = 0
    urls_detected: int = 0
    urls_redacted: int = 0
    message_ids: int = 0

    def to_dict(self) -> dict[str, int]:
        return {
            "emails": self.emails,
            "phones": self.phones,
            "tokens": self.tokens,
            "urls_detected": self.urls_detected,
            "urls_redacted": self.urls_redacted,
            "message_ids": self.message_ids,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize a Telegram export JSON file into an intermediate dataset."
    )
    parser.add_argument("--input", required=True, help="Path to Telegram export JSON")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument(
        "--chunk-gap-minutes",
        type=int,
        default=30,
        help="Time gap threshold for starting a new chunk",
    )
    parser.add_argument(
        "--max-chunk-messages",
        type=int,
        default=25,
        help="Maximum messages per chunk",
    )
    parser.add_argument(
        "--redact-urls",
        action="store_true",
        help="Replace URLs with [REDACTED_URL]. By default links are preserved.",
    )
    parser.add_argument(
        "--project-name",
        help="Project name used when building Notion-ready output.",
    )
    parser.add_argument(
        "--notion-output",
        help="If set, also create a Notion-ready package at this path.",
    )
    return parser.parse_args()


def load_export(path: Path) -> dict[str, Any]:
    if path.suffix.lower() == ".json":
        return load_json_export(path)
    if path.suffix.lower() == ".md":
        return load_toon_markdown_export(path)

    content = path.read_text(encoding="utf-8")
    stripped = content.lstrip()
    if stripped.startswith("{"):
        return load_json_export(path)
    if stripped.startswith("name:") and "messages[" in content:
        return parse_toon_markdown(content)
    raise ValueError("Unsupported export format. Expected Telegram JSON or Toon markdown.")


def load_json_export(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    messages = data.get("messages")
    if not isinstance(messages, list):
        raise ValueError("Expected top-level 'messages' array in Telegram export JSON")
    return data


def load_toon_markdown_export(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    return parse_toon_markdown(content)


def parse_toon_markdown(content: str) -> dict[str, Any]:
    lines = content.splitlines()
    export: dict[str, Any] = {}
    messages: list[dict[str, Any]] = []
    current_message: dict[str, Any] | None = None
    current_key: str | None = None
    current_type: str | None = None
    current_text_items: list[Any] = []
    pending_text_item: dict[str, Any] | None = None

    def flush_text_items() -> None:
        nonlocal current_key, current_type, current_text_items, pending_text_item
        if current_message is not None and current_key == "text":
            if pending_text_item is not None:
                current_text_items.append(pending_text_item)
                pending_text_item = None
            current_message["text"] = current_text_items.copy()
        current_key = None
        current_type = None
        current_text_items = []
        pending_text_item = None

    def flush_message() -> None:
        nonlocal current_message
        if current_message is not None:
            flush_text_items()
            messages.append(current_message)
            current_message = None

    for raw_line in lines:
        if not raw_line.strip():
            continue

        if raw_line.startswith("messages["):
            export["messages_count_hint"] = raw_line.split(":", 1)[0]
            continue

        if raw_line.startswith("  - id:"):
            flush_message()
            current_message = {"id": parse_scalar(raw_line.split(":", 1)[1].strip())}
            continue

        if current_message is None:
            if raw_line.startswith("  "):
                continue
            if ":" in raw_line:
                key, value = raw_line.split(":", 1)
                export[key.strip()] = parse_scalar(value.strip())
            continue

        if raw_line.startswith("    ") and not raw_line.startswith("      "):
            flush_text_items()
            key, value = raw_line.strip().split(":", 1)
            parsed_key = normalize_toon_key(key)
            parsed_value = value.strip()
            if key.startswith("text["):
                current_key = "text"
                current_type = "list"
                current_text_items = []
            elif parsed_key == "text":
                current_message["text"] = parse_scalar(parsed_value)
            else:
                current_message[parsed_key] = parse_scalar(parsed_value)
            continue

        if current_key == "text" and raw_line.startswith("      - "):
            item_value = raw_line.strip()[2:].strip()
            if item_value.startswith("type:"):
                if pending_text_item is not None:
                    current_text_items.append(pending_text_item)
                pending_text_item = {"type": parse_scalar(item_value.split(":", 1)[1].strip())}
            else:
                if pending_text_item is not None:
                    current_text_items.append(pending_text_item)
                    pending_text_item = None
                current_text_items.append(parse_scalar(item_value))
            continue

        if current_key == "text" and raw_line.startswith("        ") and pending_text_item is not None:
            nested = raw_line.strip()
            if ":" in nested:
                nested_key, nested_value = nested.split(":", 1)
                pending_text_item[normalize_toon_key(nested_key)] = parse_scalar(nested_value.strip())
            continue

    flush_message()
    export["messages"] = messages
    if not isinstance(export.get("messages"), list):
        raise ValueError("Expected message list in Toon markdown export")
    return export


def normalize_toon_key(key: str) -> str:
    return re.sub(r"(\[.*?\]|\{.*?\})+$", "", key).strip()


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)
    if value.isdigit():
        return int(value)
    if value in {"true", "false"}:
        return value == "true"
    return value


def flatten_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "".join(parts)
    return ""


def normalize_whitespace(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def redact_text(text: str, stats: RedactionStats, redact_urls: bool = False) -> str:
    def replace_email(match: re.Match[str]) -> str:
        stats.emails += 1
        return "[REDACTED_EMAIL]"

    def replace_phone(match: re.Match[str]) -> str:
        stats.phones += 1
        return "[REDACTED_PHONE]"

    def replace_token(match: re.Match[str]) -> str:
        token = match.group(0)
        if token.lower().startswith(("http", "message")):
            return token
        has_alpha = any(char.isalpha() for char in token)
        has_digit = any(char.isdigit() for char in token)
        if not (has_alpha and has_digit):
            return token
        stats.tokens += 1
        return "[REDACTED_TOKEN]"

    def replace_url(match: re.Match[str]) -> str:
        stats.urls_detected += 1
        if redact_urls:
            stats.urls_redacted += 1
            return "[REDACTED_URL]"
        placeholder = f"__URL_{len(url_placeholders)}__"
        url_placeholders[placeholder] = match.group(0)
        return placeholder

    def replace_message_id(match: re.Match[str]) -> str:
        stats.message_ids += 1
        return "[REDACTED_MESSAGE_ID]"

    url_placeholders: dict[str, str] = {}
    text = EMAIL_RE.sub(replace_email, text)
    text = PHONE_RE.sub(replace_phone, text)
    text = URL_RE.sub(replace_url, text)
    text = MESSAGE_ID_RE.sub(replace_message_id, text)
    text = TOKEN_RE.sub(replace_token, text)
    for placeholder, url in url_placeholders.items():
        text = text.replace(placeholder, url)
    return text


def is_noise_message(text: str, message_type: str) -> bool:
    if message_type != "message":
        return True
    if not text:
        return True
    compact = re.sub(r"\s+", "", text)
    if len(compact) < 2:
        return True
    if not re.search(r"[^\W_]", compact, re.UNICODE):
        return True
    return False


def parse_timestamp(raw_date: str | None, raw_unixtime: str | int | None) -> str | None:
    if raw_date:
        try:
            return datetime.fromisoformat(raw_date.replace("T", " ")).isoformat()
        except ValueError:
            pass
    if raw_unixtime is not None:
        try:
            stamp = int(raw_unixtime)
            return datetime.fromtimestamp(stamp, tz=timezone.utc).isoformat()
        except (TypeError, ValueError, OSError):
            return None
    return None


def category_scores(text: str) -> dict[str, int]:
    lowered = text.lower()
    scores: dict[str, int] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in lowered)
        if score:
            scores[category] = score
    return scores


def detect_category(text: str) -> tuple[str, dict[str, int]]:
    scores = category_scores(text)
    if not scores:
        return "General", {}
    return max(scores.items(), key=lambda item: item[1])[0], scores


def detect_candidate_type(text: str) -> str:
    lowered = text.lower()
    best_type = "note"
    best_score = 0
    for candidate_type, keywords in TYPE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in lowered)
        if score > best_score:
            best_type = candidate_type
            best_score = score
    return best_type


def estimate_confidence(
    text: str, candidate_type: str, category_hint_scores: dict[str, int], message_count: int
) -> str:
    score = 0
    if len(text) > 80:
        score += 1
    if message_count >= 3:
        score += 1
    if category_hint_scores:
        score += 1
    if candidate_type != "note":
        score += 1

    if score >= 4:
        return "high"
    if score >= 2:
        return "medium"
    return "low"


def summarize_keywords(text: str, limit: int = 6) -> list[str]:
    words = [word.lower() for word in WORD_RE.findall(text)]
    counter = Counter(word for word in words if word not in STOPWORDS)
    return [word for word, _count in counter.most_common(limit)]


def build_summary(text: str) -> str:
    line = text.splitlines()[0].strip()
    if len(line) <= 220:
        return line
    return f"{line[:217].rstrip()}..."


def normalize_messages(
    data: dict[str, Any], redact_urls: bool = False
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    stats = RedactionStats()
    messages_out: list[dict[str, Any]] = []
    source_counts = Counter()

    for raw in data["messages"]:
        if not isinstance(raw, dict):
            continue

        raw_text = normalize_whitespace(flatten_text(raw.get("text", "")))
        message_type = str(raw.get("type", "message"))
        is_noise = is_noise_message(raw_text, message_type)
        timestamp = parse_timestamp(raw.get("date"), raw.get("date_unixtime"))
        redacted_text = redact_text(raw_text, stats, redact_urls=redact_urls)
        category_hint, category_hint_scores = detect_category(redacted_text)

        record = {
            "message_id": raw.get("id"),
            "timestamp": timestamp,
            "sender_name": raw.get("from"),
            "sender_id": raw.get("from_id"),
            "reply_to_message_id": raw.get("reply_to_message_id"),
            "message_type": message_type,
            "has_media": bool(raw.get("media_type") or raw.get("file")),
            "media_type": raw.get("media_type"),
            "text": redacted_text,
            "category_hint": category_hint,
            "category_hint_scores": category_hint_scores,
            "is_noise": is_noise,
        }
        messages_out.append(record)
        source_counts[message_type] += 1

    useful_messages = [message for message in messages_out if not message["is_noise"]]
    audit = {
        "message_count_total": len(messages_out),
        "message_count_useful": len(useful_messages),
        "message_type_counts": dict(source_counts),
        "redactions": stats.to_dict(),
    }
    return useful_messages, audit


def group_chunks(
    messages: list[dict[str, Any]], gap_minutes: int, max_chunk_messages: int
) -> list[list[dict[str, Any]]]:
    chunks: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    previous_time: datetime | None = None

    for message in messages:
        timestamp = message.get("timestamp")
        current_time = datetime.fromisoformat(timestamp) if timestamp else None
        start_new = False

        if not current:
            start_new = True
        elif len(current) >= max_chunk_messages:
            start_new = True
        elif previous_time and current_time:
            minutes = (current_time - previous_time).total_seconds() / 60
            if minutes > gap_minutes:
                start_new = True
        elif message.get("reply_to_message_id") is None and current[-1].get("reply_to_message_id") is None:
            if message.get("sender_name") != current[-1].get("sender_name"):
                text = message.get("text", "")
                previous_text = current[-1].get("text", "")
                if not shared_keywords(text, previous_text):
                    start_new = True

        if start_new:
            if current:
                chunks.append(current)
            current = [message]
        else:
            current.append(message)

        previous_time = current_time or previous_time

    if current:
        chunks.append(current)

    return chunks


def shared_keywords(left: str, right: str) -> bool:
    left_words = set(summarize_keywords(left, limit=8))
    right_words = set(summarize_keywords(right, limit=8))
    return bool(left_words & right_words)


def chunk_record(index: int, messages: list[dict[str, Any]]) -> dict[str, Any]:
    text = "\n".join(message["text"] for message in messages if message["text"])
    categories = Counter(message["category_hint"] for message in messages if message["category_hint"])
    category = categories.most_common(1)[0][0] if categories else "General"
    category_scores_merged = Counter()
    for message in messages:
        category_scores_merged.update(message.get("category_hint_scores", {}))

    message_ids = [message["message_id"] for message in messages if message.get("message_id") is not None]
    candidate_type = detect_candidate_type(text)
    confidence = estimate_confidence(text, candidate_type, dict(category_scores_merged), len(messages))

    return {
        "chunk_id": f"chunk-{index:04d}",
        "message_count": len(messages),
        "start_timestamp": messages[0].get("timestamp"),
        "end_timestamp": messages[-1].get("timestamp"),
        "participants": sorted(
            {message["sender_name"] for message in messages if message.get("sender_name")}
        ),
        "category": category,
        "candidate_type": candidate_type,
        "confidence": confidence,
        "keywords": summarize_keywords(text),
        "summary": build_summary(text),
        "text": text,
        "source_message_ids": message_ids,
    }


def knowledge_candidate(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": record["summary"],
        "type": record["candidate_type"],
        "category": record["category"],
        "platforms": infer_platforms(record["text"]),
        "status": "needs_review",
        "confidence": record["confidence"],
        "summary": record["summary"],
        "why_it_matters": infer_impact(record["candidate_type"], record["category"]),
        "action": infer_action(record["candidate_type"]),
        "related": record["keywords"],
        "source": {
            "chunk_id": record["chunk_id"],
            "message_count": record["message_count"],
            "message_ids": record["source_message_ids"],
            "start_timestamp": record["start_timestamp"],
            "end_timestamp": record["end_timestamp"],
        },
    }


def infer_platforms(text: str) -> list[str]:
    lowered = text.lower()
    platforms: list[str] = []
    if "android" in lowered or "kotlin" in lowered:
        platforms.append("Android")
    if "ios" in lowered or "swift" in lowered:
        platforms.append("iOS")
    if "web" in lowered or "frontend" in lowered:
        platforms.append("Web")
    if "backend" in lowered or "api" in lowered or "server" in lowered:
        platforms.append("Backend")
    return platforms or ["General"]


def infer_impact(candidate_type: str, category: str) -> str:
    if candidate_type == "decision":
        return f"This likely captures an explicit {category.lower()} decision worth preserving."
    if candidate_type == "issue":
        return f"This looks like a reusable {category.lower()} problem statement or failure mode."
    if candidate_type == "task":
        return "This may indicate follow-up work or an operational handoff."
    if candidate_type == "reference":
        return "This appears to point at supporting documentation or an external source."
    if candidate_type == "question_answer":
        return "This may contain an answer to a repeated project question."
    return "This may contain reusable project context that should be reviewed."


def infer_action(candidate_type: str) -> str:
    if candidate_type == "decision":
        return "Verify the latest agreed decision and convert it into a durable knowledge item."
    if candidate_type == "issue":
        return "Confirm whether the issue is still relevant and capture root cause or workaround."
    if candidate_type == "task":
        return "Check whether the task was completed before publishing it as knowledge."
    if candidate_type == "reference":
        return "Validate the linked or referenced material and attach it if still available."
    if candidate_type == "question_answer":
        return "Promote the answer into onboarding or FAQ material if it is stable."
    return "Review manually and keep only durable knowledge."


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False))
            handle.write("\n")


def load_notion_builder():
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from build_notion_package import build_package_from_dataset

    return build_package_from_dataset


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    export = load_export(input_path)
    messages, audit = normalize_messages(export, redact_urls=args.redact_urls)
    chunks = [chunk_record(index, group) for index, group in enumerate(
        group_chunks(messages, args.chunk_gap_minutes, args.max_chunk_messages), start=1
    )]
    candidates = [knowledge_candidate(chunk) for chunk in chunks]

    write_jsonl(output_dir / "messages_normalized.jsonl", messages)
    write_jsonl(output_dir / "conversation_chunks.jsonl", chunks)
    write_jsonl(output_dir / "knowledge_candidates.jsonl", candidates)
    with (output_dir / "knowledge_dataset.json").open("w", encoding="utf-8") as handle:
        json.dump(candidates, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    category_summary = {
        "categories": dict(Counter(chunk["category"] for chunk in chunks)),
        "candidate_types": dict(Counter(chunk["candidate_type"] for chunk in chunks)),
        "confidence_levels": dict(Counter(chunk["confidence"] for chunk in chunks)),
    }

    with (output_dir / "redaction_report.json").open("w", encoding="utf-8") as handle:
        json.dump(audit, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    with (output_dir / "category_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(category_summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    if args.notion_output:
        if not args.project_name:
            raise SystemExit("--project-name is required when --notion-output is used")
        build_package_from_dataset = load_notion_builder()
        build_package_from_dataset(
            candidates,
            Path(args.notion_output),
            args.project_name,
            input_path.name,
        )


if __name__ == "__main__":
    main()
