import { LocalNotifications } from '@capacitor/local-notifications'

export async function scheduleNotification (notifyDate) {
    try {
        // Schedule a notification 
        const permission = await LocalNotifications.requestPermissions() // Request permission

        if (permission.display === 'granted') {
            const notification = await LocalNotifications.schedule({
                notifications: [
                {
                    title: 'Připravená Objednávka',
                    body: 'Vaše objednávka by nyní měla být dostupná k vyzvednutí!',
                    schedule: { at: notifyDate },
                    id: 1
                },
                ],
            });
            console.log('Notification scheduled successfully!')
            return true
        } else {
            console.log("Permission not granted!")
            return false
        }
    } catch (error) {
        console.error('Error scheduling notification', error);
        return false
    }
}