from telegram.ext import (
    ConversationHandler,
)

from solana.rpc.api import Client
from config.config_manager import CLIENT

# Import all state classes
from states import (
    StartState,
    WalletState,
    SettingsState,
    FinderState,
    StatsState,
    ListingState,
    CaseState
)

# Legacy State class for backward compatibility (deprecated)
class State:
    # Start States
    LANGUAGE_SELECTED = StartState.LANGUAGE_SELECTED.value
    SHOW_DISCLAIMER = StartState.SHOW_DISCLAIMER.value
    CHOOSE_COUNTRY = StartState.CHOOSE_COUNTRY.value
    START_CHOOSE_PROVINCE = StartState.START_CHOOSE_PROVINCE.value
    CHOOSE_PROVINCE = StartState.CHOOSE_PROVINCE.value
    CHOOSE_CITY = StartState.CHOOSE_CITY.value
    CHOOSE_ACTION = StartState.CHOOSE_ACTION.value
    CHOOSE_WALLET_TYPE = StartState.CHOOSE_WALLET_TYPE.value
    CHOOSE_OR_CREATE_WALLET = StartState.CHOOSE_OR_CREATE_WALLET.value
    NAME_WALLET = StartState.NAME_WALLET.value
    HANDLE_REPLY = StartState.HANDLE_REPLY.value
    CREATE_CASE_NAME = StartState.CREATE_CASE_NAME.value
    CREATE_CASE_MOBILE = StartState.CREATE_CASE_MOBILE.value
    CREATE_CASE_TAC = StartState.CREATE_CASE_TAC.value
    CREATE_CASE_DISCLAIMER = StartState.CREATE_CASE_DISCLAIMER.value
    CREATE_CASE_REWARD_TYPE = StartState.CREATE_CASE_REWARD_TYPE.value
    CREATE_CASE_REWARD_AMOUNT = StartState.CREATE_CASE_REWARD_AMOUNT.value
    CREATE_CASE_PERSON_NAME = StartState.CREATE_CASE_PERSON_NAME.value
    CREATE_CASE_RELATIONSHIP = StartState.CREATE_CASE_RELATIONSHIP.value
    CREATE_CASE_PHOTO = StartState.CREATE_CASE_PHOTO.value
    CREATE_CASE_LAST_SEEN_LOCATION = StartState.CREATE_CASE_LAST_SEEN_LOCATION.value
    CREATE_CASE_SEX = StartState.CREATE_CASE_SEX.value
    CREATE_CASE_AGE = StartState.CREATE_CASE_AGE.value
    CREATE_CASE_HAIR_COLOR = StartState.CREATE_CASE_HAIR_COLOR.value
    CREATE_CASE_EYE_COLOR = StartState.CREATE_CASE_EYE_COLOR.value
    CREATE_CASE_HEIGHT = StartState.CREATE_CASE_HEIGHT.value
    CREATE_CASE_WEIGHT = StartState.CREATE_CASE_WEIGHT.value
    CREATE_CASE_DISTINCTIVE_FEATURES = StartState.CREATE_CASE_DISTINCTIVE_FEATURES.value
    CREATE_CASE_SUBMIT = StartState.CREATE_CASE_SUBMIT.value
    CREATE_CASE_ASK_REASON = StartState.CREATE_CASE_ASK_REASON.value
    CREATE_CASE_ASK_REWARD = StartState.CREATE_CASE_ASK_REWARD.value
    CREATE_CASE_CONFIRM_TRANSFER = StartState.CREATE_CASE_CONFIRM_TRANSFER.value
    CREATE_CASE_FINISHED = StartState.CREATE_CASE_FINISHED.value
    CASE_LIST = StartState.CASE_LIST.value
    CASE_DETAILS = StartState.CASE_DETAILS.value
    UPLOAD_PROOF = StartState.UPLOAD_PROOF.value
    ENTER_LOCATION = StartState.ENTER_LOCATION.value
    EXTEND_REWARD = StartState.EXTEND_REWARD.value
    CONFIRM_FOUND = StartState.CONFIRM_FOUND.value
    EXTEND_REWARD_AMOUNT = StartState.EXTEND_REWARD_AMOUNT.value
    ADVERTISER_RESPONSE = StartState.ADVERTISER_RESPONSE.value
    FINDER_CHOOSE_WALLET_TYPE = StartState.FINDER_CHOOSE_WALLET_TYPE.value
    FINDER_NAME_WALLET = StartState.FINDER_NAME_WALLET.value
    FINDER_CONFIRM_TRANSACTION = StartState.FINDER_CONFIRM_TRANSACTION.value
    TRANSFER_CONFIRMATION = StartState.TRANSFER_CONFIRMATION.value
    CONFIRM_EXTEND = StartState.CONFIRM_EXTEND.value
    ENTER_COUNTRY = StartState.ENTER_COUNTRY.value
    ENTER_CITY = StartState.ENTER_CITY.value
    EDIT_FIELD = StartState.EDIT_FIELD.value
    REWARD_TRANSFER_PROCESS = StartState.REWARD_TRANSFER_PROCESS.value
    FINISHED = StartState.FINISHED.value
    EXTEND_REWARD_CONFIRM = StartState.EXTEND_REWARD_CONFIRM.value
    EXTEND_REWARD_FINISHED = StartState.EXTEND_REWARD_FINISHED.value
    EXTEND_REWARD_ASK_REASON = StartState.EXTEND_REWARD_ASK_REASON.value
    SELECT_WALLET_FOR_EXTEND = StartState.SELECT_WALLET_FOR_EXTEND.value
    ENTER_WALLET_NAME = StartState.ENTER_WALLET_NAME.value
    SELECT_WALLET_TYPE = StartState.SELECT_WALLET_TYPE.value
    CONFIRM_REWARD = StartState.CONFIRM_REWARD.value
    
    # Case States
    ENTER_PRIVATE_KEY = CaseState.ENTER_PRIVATE_KEY.value
    ENTER_PUBLIC_KEY = CaseState.ENTER_PUBLIC_KEY.value
    CONFIRM_TRANSFER = CaseState.CONFIRM_TRANSFER.value
    CREATE_CASE_WALLET_TRANSFER = CaseState.CREATE_CASE_WALLET_TRANSFER.value
    CREATE_CASE_CONFIRM_TRANSFER = CaseState.CREATE_CASE_CONFIRM_TRANSFER.value
    CREATE_CASE_ASK_REWARD = CaseState.CREATE_CASE_ASK_REWARD.value
    WALLET_MENU = CaseState.WALLET_MENU.value
    WAITING_FOR_MOBILE = CaseState.WAITING_FOR_MOBILE.value
    CREATE_WALLET = CaseState.CREATE_WALLET.value
    SELECT_WALLET = CaseState.SELECT_WALLET.value
    ADVERTISER_CONFIRMATION = CaseState.ADVERTISER_CONFIRMATION.value
    MOBILE_VERIFICATION = CaseState.MOBILE_VERIFICATION.value
    SETTINGS_MENU = CaseState.SETTINGS_MENU.value
    MOBILE_MANAGEMENT = CaseState.MOBILE_MANAGEMENT.value
    HISTORY_MENU = CaseState.HISTORY_MENU.value
    ENTER_NUMBER = CaseState.ENTER_NUMBER.value
    VERIFY_OTP = CaseState.VERIFY_OTP.value
    VIEW_HISTORY = CaseState.VIEW_HISTORY.value
    DELETE_WALLET = CaseState.DELETE_WALLET.value
    SHOW_ADDRESS = CaseState.SHOW_ADDRESS.value
    HANDLER_END = CaseState.HANDLER_END.value
    END = -1

    # Legacy nested classes for backward compatibility
    class FINDER:
        CREATE_CASE_MOBILE = FinderState.CREATE_CASE_MOBILE.value
        MOBILE_MANAGEMENT = FinderState.MOBILE_MANAGEMENT.value
        CREATE_CASE_TAC = FinderState.CREATE_CASE_TAC.value
        FINDER_DISCLAIMER = FinderState.FINDER_DISCLAIMER.value
        CHOOSE_COUNTRY = FinderState.CHOOSE_COUNTRY.value
        CHOOSE_PROVINCE = FinderState.CHOOSE_PROVINCE.value
        VIEW_COMPLAINTS = FinderState.VIEW_COMPLAINTS.value
        END = FinderState.END.value

    class WALLETS:
        WALLET_MENU = WalletState.WALLET_MENU.value
        SOL_WALLET_DETAIL = WalletState.SOL_WALLET_DETAIL.value
        SOL_WALLET_ACTIONS = WalletState.SOL_WALLET_ACTIONS.value
        USDT_WALLET_DETAIL = WalletState.USDT_WALLET_DETAIL.value
        USDT_WALLET_ACTIONS = WalletState.USDT_WALLET_ACTIONS.value
        CONFIRM_PRIVATE_KEY = WalletState.CONFIRM_PRIVATE_KEY.value
        SHOW_ADDRESS = WalletState.SHOW_ADDRESS.value
        VIEW_HISTORY = WalletState.VIEW_HISTORY.value
        SELECT_WALLET_TYPE = WalletState.SELECT_WALLET_TYPE.value
        ENTER_WALLET_NAME = WalletState.ENTER_WALLET_NAME.value
        CONFIRM_DELETE_WALLET = WalletState.CONFIRM_DELETE_WALLET.value
        DELETE_WALLET = WalletState.DELETE_WALLET.value
        END = WalletState.END.value

    class SETTINGS:
        SETTINGS_MENU = SettingsState.SETTINGS_MENU.value
        WAITING_FOR_MOBILE = SettingsState.WAITING_FOR_MOBILE.value
        SETTINGS_MOBILE_MANAGEMENT = SettingsState.SETTINGS_MOBILE_MANAGEMENT.value
        MOBILE_VERIFICATION = SettingsState.MOBILE_VERIFICATION.value
        SETTINGS_CREATE_CASE_TAC = SettingsState.SETTINGS_CREATE_CASE_TAC.value
        END = SettingsState.END.value

# ======================
# Language Data & Constants
# ======================

DUMMY_DATA = {
    "en": {
        "mobile_saved": "✅ Mobile number saved: {number}",
        # Case Functionality
        "create_case_title": "<b>Case Details</b>",
        "enter_name": "👤 Enter the full name of the person you're looking for:",
        "disclaimer_2": (
            "Disclaimer 2:\n\n"
            "1. The reward amount will be held in escrow until the case is resolved.\n"
            "2. Misuse of this service is prohibited.\n"
            "3. All information provided will be publicly visible.\n\n"
            "Do you agree?"
        ),
        "enter_reward_amount": "Enter the reward amount:",
        "insufficient_funds": "Insufficient funds. Please top up your wallet.",
        "top_up_tutorial": (
            "How to top up your wallet:\n"
            "1. Open your Solana wallet app (e.g., Phantom, Solflare).\n"
            "2. Copy your wallet address: {address}\n"
            "3. Send at least {amount} SOL to the address."
        ),
        "enter_person_name": "Enter the name of the person you're looking for:",
        "relationship": "Your relationship to the person:",
        "upload_photo": "Upload a clear photo of the person:",
        "last_seen_location": "Enter the last seen location (province):",
        "sex": "Sex (Male/Female):",
        "age": "Age:",
        "hair_color": "Hair Color:",
        "eye_color": "Eye Color:",
        "height": "Height (cm):",
        "weight": "Weight (kg):",
        "distinctive_features": "Distinctive physical features (e.g., Tattoo of eagle):",
        "reason_for_finding": "Reason for finding:",
        "submit_case": "Submit Case",
        "case_submitted": "✅ Case submitted successfully!\nCase Number: {case_no}",
        "case_failed": "❌ Failed to submit case. Please try again.",
        "escrow_transfer": "Reward amount transferred to escrow wallet.",
        # Find People Functionality
    },
    "zh": {
        "menu_settings_title": "设置菜单",
        "btn_language": "更改语言",
        "btn_mobile_number": "手机号",
        "btn_close_menu": "关闭菜单",
        "mobile_saved": "✅ 已保存手机号：{number}",
        "lang_updated": "语言已更新。",
        # Case Functionality
        "create_case_title": "创建新案件",
        "enter_name": "请输入您的姓名：",
        "enter_tac": "请输入发送到您手机的验证码：",
        "verify_tac": "正在验证验证码...",
        "tac_verified": "✅ 验证码验证成功。",
        "tac_invalid": "❌ 验证码无效，请重试。",
        "disclaimer_2": (
            "免责声明 2:\n\n"
            "1. 赏金金额将托管至案件解决。\n"
            "2. 禁止滥用本服务。\n"
            "3. 提供的所有信息将公开可见。\n\n"
            "您是否同意？"
        ),
        "enter_reward_amount": "请输入赏金金额：",
        "insufficient_funds": "余额不足，请充值钱包。",
        "top_up_tutorial": (
            "如何充值钱包：\n"
            "1. 打开您的 Solana 钱包应用（例如 Phantom、Solflare）。\n"
            "2. 复制您的钱包地址：{address}\n"
            "3. 向该地址发送至少 {amount} SOL。"
        ),
        "enter_person_name": "请输入您要寻找的人的姓名：",
        "relationship": "您与该人的关系：",
        "upload_photo": "上传清晰的人物照片：",
        "last_seen_location": "请输入最后出现的位置（省份）：",
        "sex": "性别（男/女）：",
        "age": "年龄：",
        "hair_color": "发色：",
        "eye_color": "眼睛颜色：",
        "height": "身高（厘米）：",
        "weight": "体重（公斤）：",
        "distinctive_features": "显著的身体特征（例如，鹰形纹身）：",
        "reason_for_finding": "寻找原因：",
        "submit_case": "提交案件",
        "case_submitted": "✅ 案件提交成功！\n案件编号：{case_no}",
        "case_failed": "❌ 提交案件失败，请重试。",
        "escrow_transfer": "赏金金额已转入托管钱包。",
        # Find People Functionality
        "choose_province": "请选择省份：",
        "more_provinces": "更多省份...",
        "case_list": "可用案件：",
        "case_details": "案件详情：",
        "save_case": "保存案件",
        "found_case": "找到案件",
        "upload_proof": "请上传照片或视频作为证据。",
        "invalid_proof": "无效证据。请上传照片或视频。",
        "enter_location": "请输入发现该人的地点：",
        "notify_advertiser": "已通知广告主。谢谢！",
        "province_not_found": "未找到匹配的省份。请重试：",
        "province_multi": "找到多个省份 (第 {page} 页，共 {total} 页)：",
        "province_selected": "已记录省份：",
        "missing_information": "❌ 缺少信息。请重新开始。",
        "notification_text": (
            "🚨 潜在匹配警报！🚨\n\n"
            "案件 #{case_no}: {person_name}\n"
            "📍 报告位置: {location}\n"
            "🔗 证据文件: {proof_path}"
        ),
        "reply_to_advertiser": "✅ 案件所有者已收到通知！\n\n"
        "感谢您的贡献。如果需要更多信息，我们会联系您。",
        "error_sending_notification": "❌ 发送通知时出错。请稍后再试。",
        "proof_upload": "请上传照片/视频证据：",
        "error_processing_proof": "❌ 处理您的证据时出错。请重试。",
        "case_not_found": "❌ 未找到案件。",
        "proof_received": "✅ 证据已收到。\n\n请输入您发现此人的位置：",
        "error_upload_proof": "❌ 请上传照片或视频。",
        "no_case_selected": "错误: 未选择案件。请重新开始。",
        "error_loading_case": "加载案件详情时出错，请重试。",
        "mark_as_found": "✅ 标记为已找到",
        "back_to_list": "🔙 返回列表",
        "case_not_found_in_province": "该省份未找到案件。",
        "select_province": "请先选择一个省份。",
        "no_case_found_in_province": "在 {province} 没有找到相关案件。",
        "choose_number_or_add_new": "选择一个号码或添加新号码：",
        "add_new_number": "添加新号码",
        "enter_new_number": "请输入一个新号码：",
        "number_already_exists": "号码 <b>{number}</b> 已存在。",
        "otp_sent": "已向 <b>{number}</b> 发送验证码。请输入验证码以验证。",
        "number_added": "号码 <b>{number}</b> 已成功添加。",
        "invalid_otp": "无效的验证码。请重试。",
    },
}

WALLETS_DIR = "wallets"  # Directory to store user wallets
PHOTOS_DIR = "photos"  # Directory to store uploaded photos
PROOFS_DIR = "proofs"  # Directory to store proof uploads
USDT_CONTRACT = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"

# ====================== Solana ======================

solana_client = Client(CLIENT)