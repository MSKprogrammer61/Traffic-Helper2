import discord
from discord.ext import commands
from model import get_all_predictions
from model import preprocess_image

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Başarılı Bir Şekilde Sunucuya İntikal Ettik{bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Merhaba! Ben{bot.user}! Size En İyi Şekilde Yardım Edeceğim.')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                await ctx.send("Sadece *.jpg, .jpeg veya .png* formatında dosya gönderebilirsin!")
                continue  # Bu dosyayı atla, diğerlerine bak

            await attachment.save(f"./{attachment.filename}")

            try:
                all_preds = get_all_predictions(
                    model_path="keras_model.h5",
                    labels_path="labels.txt",
                    image_path=f"./{attachment.filename}"
                )

                # En iyi tahmini al
                best_label, best_conf = all_preds[0]
                response = f"Bu fotoğraf bana *{best_conf}% ihtimalle {best_label}* gibi görünüyor!\n\n"
                response += "*Tüm tahminler:*\n"

                for label, pct in all_preds:
                    response += f"- {label}: %{pct}\n"

                # Discord mesajı 2000 karakter sınırı var, çok uzunsa böl
                if len(response) > 1900:
                    response = response[:1900] + "... (kısaltıldı)"

                await ctx.send(response)

            except Exception as e:
                await ctx.send(f"Bir hata oluştu: {str(e)}")

    else:
        await ctx.send("Lütfen bir resim dosyası ekle!")

        
@bot.command()
async def Neden_Bu_Sunucu_Kuruldu(ctx):
    await ctx.send("Bu sunucu Kodland Pro Kursumda discord ai yaparken kurduğum benim için çok önemli ve değerli bir sunucudur çünkü hocalarımın bana verdiği kıymet ve değer vermesiyle oluşmuş bir sunucudur. Benim Hocalarım: Ayşenur Hocam, Faruk Hocam, Eski Python Kursumda bana eşlik edip bitirmemi sağlayan ve kendisine minnettar olduğum Ahmet ÇAĞLAR Hocam.")

@bot.command()
async def Sunucunun_Amacı_Nedir(ctx):
    await ctx.send("Araçlarda,yollarda veya herhangi bir toplum içi bir alanda uykulu gözlerin veya kamburluk derecesine bakan bir ai discord botu oluşturmak.")


        
bot.run("")