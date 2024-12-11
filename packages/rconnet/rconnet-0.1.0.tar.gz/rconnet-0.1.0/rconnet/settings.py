import re

class Settings():
    def __init__(self, client):
        self.__client = client

    def __is_valid_ip(self, ip):
        ip_regex = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        if re.match(ip_regex, ip):
            return True
        else:
            return False

    def __setting(self, type_option: str, option: str, value: object):

        if type_option == "str":
            if value is None:
                return self.__client.rcon_invoke("exec %s" % (option))
            return self.__client.rcon_invoke("exec %s \"%s\"" % (option, value))
        elif type_option == "bool":
            if value is None:
                return bool(int(self.__client.rcon_invoke("exec %s" % (option))))
            if bool(value) is True:
                value = "1"
            else:
                value = "0"
            return self.__client.rcon_invoke("exec %s \"%s\"" % (option, value))
        elif type_option == "int":
            if value is None:
                return self.__client.rcon_invoke("exec %s" % (option))
            if not isinstance(value, int): raise Exception("Wrong data type. Integer")
            return self.__client.rcon_invoke("exec %s \"%s\"" % (option, value))
        elif type_option == "float":
            if value is None:
                return self.__client.rcon_invoke("exec %s" % (option))
            if not isinstance(value, float): raise Exception("Wrong data type. Float")
            return self.__client.rcon_invoke("exec %s \"%s\"" % (option, value))

    def server_name(self, value: str=None):
        return self.__setting("int", "sv.serverName", value)

    def password(self, value: str=None):
        return self.__setting("str", "sv.password", value)

    def internet(self, value: bool=None):
        return self.__setting("bool", "sv.internet", value)

    def bandwidth_choke(self, value: bool=None):
        return self.__setting("bool", "sv.bandwidthChoke", value)

    def server_ip(self, value: str=None):
        if value is not None and not self.__is_valid_ip(value): Exception("IP address of the server is incorrect.")
        return self.__setting("str", "sv.serverIP", value)

    def server_port(self, value: int=None):
        return self.__setting("int", "sv.serverPort", value)

    def welcome_message(self, value: str=None):
        return self.__setting("str", "sv.welcomeMessage", value)

    def punk_buster(self, value: bool=None):
        return self.__setting("bool", "sv.punkBuster", value)

    def allow_free_cam(self, value: bool=None):
        return self.__setting("bool", "sv.allowFreeCam", value)

    def allow_external_views(self, value: bool=None):
        return self.__setting("bool", "sv.allowExternalViews", value)

    def allow_nose_cam(self, value: bool=None):
        return self.__setting("bool", "sv.allowNoseCam", value)

    def hit_indicator(self, value: bool=None):
        return self.__setting("bool", "sv.hitIndicator", value)

    def max_players(self, value: int=None):
        return self.__setting("int", "sv.maxPlayers", value)

    def num_players_needed_to_start(self, value: int=None):
        return self.__setting("int", "sv.numPlayersNeededToStart", value)

    def not_enough_players_restart_delay(self, value: int=None):
        return self.__setting("int", "sv.notEnoughPlayersRestartDelay", value)

    def start_delay(self, value: int=None):
        return self.__setting("int", "sv.startDelay", value)

    def end_delay(self, value: int=None):
        return self.__setting("int", "sv.endDelay", value)

    def spawn_time(self, value: int=None):
        return self.__setting("int", "sv.spawnTime", value)

    def man_down_time(self, value: int=None):
        return self.__setting("int", "sv.manDownTime", value)

    def end_round_delay(self, value: int=None):
        return self.__setting("int", "sv.endOfRoundDelay", value)

    def ticket_ratio(self, value: int=None):
        return self.__setting("int", "sv.ticketRatio", value)

    def rounds_per_map(self, value: int=None):
        return self.__setting("int", "sv.roundsPerMap", value)

    def time_limit(self, value: int=None):
        return self.__setting("int", "sv.timeLimit", value)

    def score_limit(self, value: int=None):
        return self.__setting("int", "sv.scoreLimit", value)

    def soldier_friendly_fire(self, value: int=None):
        return self.__setting("int", "sv.soldierFriendlyFire", value)

    def vehicle_friendly_Fire(self, value: int=None):
        return self.__setting("int", "sv.vehicle_friendly_Fire", value)

    def soldier_splash_friendly_fire(self, value: int=None):
        return self.__setting("int", "sv.soldierSplashFriendlyFire", value)

    def vehicle_splash_friendly_fire(self, value: int=None):
        return self.__setting("int", "sv.vehicleSplashFriendlyFire", value)

    def tk_punish_enabled(self, value: bool=None):
        return self.__setting("bool", "sv.tkPunishEnabled", value)

    def tk_num_punish_to_kick(self, value: int=None):
        return self.__setting("int", "sv.tkNumPunishToKick", value)

    def tk_punish_by_default(self, value: int=None):
        return self.__setting("int", "sv.tkPunishByDefault", value)

    def voting_enabled(self, value: bool=None):
        return self.__setting("bool", "sv.votingEnabled", value)

    def vote_time(self, value: int=None):
        return self.__setting("int", "sv.voteTime", value)

    def min_players_for_voting(self, value: int=None):
        return self.__setting("int", "sv.minPlayersForVoting", value)

    def game_spy_port(self, value: int=None):
        return self.__setting("int", "sv.gameSpyPort", value)

    def allow_NAT_Negotiation(self, value: bool=None):
        return self.__setting("bool", "sv.allowNATNegotiation", value)

    def interface_IP(self, value: str=None):
        if value is not None and not self.__is_valid_ip(value): Exception("Interface IP is incorrect.")
        return self.__setting("str", "sv.interfaceIP", value)

    def auto_record(self, value: bool=None):
        return self.__setting("bool", "sv.autoRecord", value)

    def demo_index_URL(self, value: str=None):
        return self.__setting("str", "sv.demoIndexURL", value)

    def demo_download_URL(self, value: str=None):
        return self.__setting("str", "sv.demoDownloadURL", value)

    def auto_demo_hook(self, value: str=None):
        return self.__setting("str", "sv.autoDemoHook", value)

    def demo_Quality(self, value: int=None):
        return self.__setting("int", "sv.demoQuality", value)

    def admin_script(self, value: str=None):
        return self.__setting("str", "sv.adminScript", value)

    def time_before_restart_map(self, value: int=None):
        return self.__setting("int", "sv.timeBeforeRestartMap", value)

    def auto_balance_team(self, value: bool=None):
        return self.__setting("bool", "sv.autoBalanceTeam", value)

    def team_ratio_percent(self, value: int=None):
        return self.__setting("int", "sv.teamRatioPercent", value)

    def voip_enabled(self, value: bool=None):
        return self.__setting("bool", "sv.voipEnabled", value)

    def voip_quality(self, value: int=None):
        return self.__setting("int", "sv.voipQuality", value)

    def voip_server_remote(self, value: bool=None):
        return self.__setting("bool", "sv.voipServerRemote", value)

    def voip_server_remote_IP(self, value: str=None):
        if value is not None and not self.__is_valid_ip(value): Exception("Voip server remote IP is incorrect.")
        return self.__setting("str", "sv.voipServerRemoteIP", value)

    def voip_server_port(self, value: int=None):
        return self.__setting("int", "sv.voipServerPort", value)

    def voip_BF_client_port(self, value: int=None):
        return self.__setting("int", "sv.voipBFClientPort", value)

    def voip_BF_server_Port(self, value: int=None):
        return self.__setting("int", "sv.voipBFServerPort", value)

    def voip_hared_password(self, value: str=None):
        return self.__setting("str", "sv.voipSharedPassword", value)

    def use_global_rank(self, value: bool=None):
        return self.__setting("bool", "sv.useGlobalRank", value)

    def use_global_unlocks(self, value: bool=None):
        return self.__setting("bool", "sv.useGlobalUnlocks", value)

    def min_unlock_level(self, value: int=None):
        return self.__setting("int", "sv.minUnlockLevel", value)

    def max_unlock_level(self, value: int=None):
        return self.__setting("int", "sv.maxUnlockLevel", value)

    def sponsor_text(self, value: str=None):
        return self.__setting("str", "sv.sponsorText", value)

    def sponsor_logo_url(self, value: str=None):
        return self.__setting("str", "sv.sponsorLogoURL", value)

    def community_logo_url(self, value: str=None):
        return self.__setting("str", "sv.communityLogoURL", value)

    def custom_map_url(self, value: int=None):
        return self.__setting("int", "sv.customMapURL", value)

    def radio_spam_interval(self, value: int=None):
        return self.__setting("int", "sv.radioSpamInterval", value)

    def radio_max_spam_flag_count(self, value: int=None):
        return self.__setting("int", "sv.radioMaxSpamFlagCount", value)

    def radio_blocked_duration_time(self, value: int=None):
        return self.__setting("int", "sv.radioBlockedDurationTime", value)

    def max_rank(self, value: int=None):
        return self.__setting("int", "sv.maxRank", value)

    def allow_spectators(self, value: bool=None):
        return self.__setting("bool", "sv.allowSpectators", value)

    def allow_titan_movement(self, value: int=None):
        return self.__setting("int", "sv.allowTitanMovement", value)

    def bot_skill(self, value: float=None):
        return self.__setting("float", "sv.botSkill", value)