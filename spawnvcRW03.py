@bot.event
async def on_voice_state_update(member, before, after):
    bcmdn = member.display_name
    if '#' in bcmdn:
        mnn = bcmdn[0:bcmdn.find('#')]
    else: mnn = bcmdn
    print(f"\n\r{datetime.now() + timedelta(hours=Hours)} activity detected  {mnn} 01")
    print(f"{datetime.now() + timedelta(hours=Hours)} before  {before.channel} 00")
    print(f"{datetime.now() + timedelta(hours=Hours)} after  {after.channel} 00")
    
    if after.channel is not None and after.channel.name == 'MakeNewChannel':
        print(f"{datetime.now() + timedelta(hours=Hours)} after  {after.channel} 02")
        category = after.channel.category
        bcmdn = member.display_name

        if '#' in bcmdn:
            mnn = bcmdn[0:bcmdn.find('#')]
        else: mnn = bcmdn
        
        new_channel = await category.create_voice_channel(f"VCX {mnn}")
        time.sleep(.1);
        await member.move_to(new_channel)
        time.sleep(.1);
        print(f"{datetime.now() + timedelta(hours=Hours)} member moved 03")

    if before.channel is not None and 'VCX' in str({before.channel}):
        print(f"{datetime.now() + timedelta(hours=Hours)} before  {before.channel} 04")
        if len(before.channel.members) == 0:
            await before.channel.delete()
            time.sleep(.1);
            print(f"{datetime.now() + timedelta(hours=Hours)} channel deleted 05")
        else:
            bcmdn = before.channel.members[0].display_name

            if '#' in bcmdn:
                mnn = bcmdn[0:bcmdn.find('#')]
            else: mnn = bcmdn
            print(f"{datetime.now() + timedelta(hours=Hours)} before  {before.channel} 06")
            await before.channel.edit(name = f"VCX {mnn}")
            time.sleep(.1);
            print(f"{datetime.now() + timedelta(hours=Hours)} channel renamed VCX {mnn} 07")
    
    print(f"{datetime.now() + timedelta(hours=Hours)} before  {before.channel} 08")
    print(f"{datetime.now() + timedelta(hours=Hours)} after  {after.channel} 09")
