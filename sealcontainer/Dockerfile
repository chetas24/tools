# Use Windows base image
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Set working directory
WORKDIR /sealcontainer

# Copy all files into container
COPY . .

# Set PATH
ENV PATH="C:\\sealcontainer\\;$PATH"

# Create 'thanos' user with admin rights
RUN net user thanos thanos /add && \
    net localgroup Administrators thanos /add

# Change ownership of thanos.bat to thanos user only (restrict access)
RUN icacls "thanos.bat" /inheritance:r && \
    icacls "thanos.bat" /grant thanos:F /deny "Users:(R)" /T

# Run as thanos user using runas command
CMD ["cmd.exe", "/c", "runas /user:thanos \"cmd /c thanos.bat\""]
