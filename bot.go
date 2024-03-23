package main

import (
	"log"
	"time"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/jasonlvhit/gocron"
)

// Configuration parameters
const (
	Token            = "6765987978:AAHuqASdsQPFUV2O28nbx9nbM0QbTwHKL4U"
	SourceChannelID  = -1002023444138 // Replace with your source channel ID
	TargetChannelID  = -1002059668597 // Replace with your target channel ID
	ForwardBatchSize = 6
	ForwardInterval  = 10 // in minutes
)

func main() {
	bot, err := tgbotapi.NewBotAPI(Token)
	if err != nil {
		log.Fatal(err)
	}

	log.Printf("Authorized on account %s", bot.Self.UserName)

	// Fetch and forward messages from source channel
	fetchAndForwardMessages(bot)

	// Schedule forwarding every 10 minutes
	gocron.Every(ForwardInterval).Minutes().Do(fetchAndForwardMessages, bot)

	// Run the scheduler
	<-gocron.Start()

	// Keep the program running
	select {}
}

func fetchAndForwardMessages(bot *tgbotapi.BotAPI) {
	// Get all messages from source channel
	allMessages, err := getAllMessages(bot)
	if err != nil {
		log.Printf("Error fetching messages: %v", err)
		return
	}

	// Forward videos to target channel in batches
	for i := 0; i < len(allMessages); i += ForwardBatchSize {
		end := i + ForwardBatchSize
		if end > len(allMessages) {
			end = len(allMessages)
		}

		batch := allMessages[i:end]
		for _, message := range batch {
			if message.Video != nil {
				forwardMsg := tgbotapi.NewForward(TargetChannelID, SourceChannelID, message.MessageID)
				if _, err := bot.Send(forwardMsg); err != nil {
					log.Printf("Error forwarding message: %v", err)
				}
			}
		}

		// Sleep for 10 minutes
		time.Sleep(ForwardInterval * time.Minute)
	}
}

func getAllMessages(bot *tgbotapi.BotAPI) ([]tgbotapi.Message, error) {
	var allMessages []tgbotapi.Message
	offset := 0
	limit := 100
	for {
		messages, err := bot.GetChatHistory(tgbotapi.ChatConfig{ChatID: SourceChannelID, Limit: limit, Offset: offset})
		if err != nil {
			return nil, err
		}
		if len(messages.Messages) == 0 {
			break
		}
		allMessages = append(allMessages, messages.Messages...)
		offset += len(messages.Messages)
	}
	return allMessages, nil
}
