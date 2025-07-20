    def cleanup(self):
        """Clean up resources and restore system state"""
        self.logger.info("Starting cleanup...")
        
        # Stop any active scanning
        self.scanning = False
        if self.packet_capture_thread and self.packet_capture_thread.is_alive():
            self.packet_capture_thread.join(timeout=2)
        
        # Disable monitor mode if it was enabled
        if self.monitor_mode:
            console.print("Disabling monitor mode...", style="yellow")
            self.disable_monitor_mode()
        
        # Save final game state
        if self.config['auto_save']:
            self.save_player_data()
        
        # Close audio
        try:
            pygame.mixer.quit()
        except:
            pass
        
        self.logger.info("Cleanup completed")
        console.print("✅ Cleanup completed. Thanks for playing! 🎮", style="green")
    def cleanup(self):
        """Clean up resources and restore system state"""
        self.logger.info("Starting cleanup...")
        
        # Stop any active scanning
        self.scanning = False
        if self.packet_capture_thread and self.packet_capture_thread.is_alive():
            self.packet_capture_thread.join(timeout=2)
        
        # Disable monitor mode if it was enabled
        if self.monitor_mode:
            console.print("Disabling monitor mode...", style="yellow")
            self.disable_monitor_mode()
        
        # Save final game state
        if self.config['auto_save']:
            self.save_player_data()
        
        # Close audio
        try:
            pygame.mixer.quit()
        except:
            pass
        
        self.logger.info("Cleanup completed")
        console.print("✅ Cleanup completed. Thanks for playing! 🎮", style="green")
