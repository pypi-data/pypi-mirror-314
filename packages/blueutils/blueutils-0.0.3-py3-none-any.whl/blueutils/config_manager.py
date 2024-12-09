import configparser
import os
from loguru import logger

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        # 如果配置文件不存在，则创建空的配置文件
        if not os.path.exists(self.config_file):
            logger.warning(f"配置文件 {self.config_file} 不存在，创建空配置文件...")
            self.create_empty_config()
        else:
            self.load_config()

    def create_empty_config(self, encoding='utf-8'):
        """创建空的配置文件"""
        # 创建空文件，但不添加任何内容
        with open(self.config_file, 'w', encoding=encoding) as configfile:
            pass
        logger.info(f"空配置文件已创建：{self.config_file}")

    def load_config(self, encoding='utf-8'):
        """加载配置文件"""
        self.config.read(self.config_file, encoding=encoding)
        logger.info(f"已加载配置文件：{self.config_file}")

    def get(self, section, option, fallback=None):
        """获取配置项，若不存在则使用 fallback"""
        return self.config.get(section, option, fallback=fallback)

    def get_int(self, section, option, fallback=None):
        """获取整数配置项，若不存在则使用 fallback"""
        return self.config.getint(section, option, fallback=fallback)

    def get_float(self, section, option, fallback=None):
        """获取浮点数配置项，若不存在则使用 fallback"""
        return self.config.getfloat(section, option, fallback=fallback)

    def get_bool(self, section, option, fallback=None):
        """获取布尔值配置项，若不存在则使用 fallback"""
        return self.config.getboolean(section, option, fallback=fallback)

    def add_section(self, section):
        """动态添加新配置节"""
        if not self.config.has_section(section):
            self.config.add_section(section)
    
    def _convert_value(self, value):
        if isinstance(value, str):
            return value
        elif isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(value)
        elif isinstance(value, bool):
            return str(value).lower()
        else:
            logger.error(f"不支持的值类型: {type(value)}，请使用字符串、整数、浮点数或布尔值。")
            return None

    def set(self, section, option, value):
        """设置或更新配置项，但如果项已存在则不覆盖，并检查类型"""
        if not self.config.has_section(section):
            self.add_section(section)

        converted_value = self._convert_value(value)
        if converted_value is not None:
            if not self.config.has_option(section, option):
                logger.info(f"设置配置项 '{option}' 在节 '{section}' 中的值为 '{value}'")
                self.config.set(section, option, converted_value)
            # else:
            #     logger.warning(f"配置项 '{option}' 在节 '{section}' 中已存在，跳过设置。")

    def save(self):
        """保存配置到文件"""
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        logger.info(f"配置文件已保存：{self.config_file}")

    def remove_option(self, section, option):
        """删除配置项"""
        if self.config.has_section(section):
            self.config.remove_option(section, option)

    def remove_section(self, section):
        """删除整个配置节"""
        if self.config.has_section(section):
            self.config.remove_section(section)


# 使用示例
if __name__ == "__main__":
    config_file = "config.ini"
    config_manager = ConfigManager(config_file)

    # 读取配置项
    db_host = config_manager.get('database', 'host', fallback='localhost')
    db_port = config_manager.get_int('database', 'port', fallback=5432)
    db_user = config_manager.get('database', 'user', fallback='admin')
    log_level = config_manager.get('logging', 'log_level', fallback='INFO')

    logger.info(f"Database Host: {db_host}")
    logger.info(f"Database Port: {db_port}")
    logger.info(f"Database User: {db_user}")
    logger.info(f"Log Level: {log_level}")

    # 设置新配置项（如果项不存在）
    config_manager.set('database', 'max_connections', '100')

    # 保存到文件
    config_manager.save()